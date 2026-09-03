"""
OrderFlow API — Flask backend demo for order management.
Built by Neoux Industrial Solutions.

Run locally:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "orderflow-demo-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'orderflow.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


# ---------------------------------------------------------------- MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(40), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "sku": self.sku,
            "price": self.price, "stock": self.stock,
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(30), default="pending")  # pending / processing / shipped / delivered / cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "product": self.product.name if self.product else None,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------------------------------------------------- REST API ---
@app.route("/api/products", methods=["GET"])
def api_list_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@app.route("/api/products", methods=["POST"])
def api_create_product():
    data = request.get_json(force=True)
    p = Product(
        name=data["name"], sku=data["sku"],
        price=float(data["price"]), stock=int(data.get("stock", 0)),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@app.route("/api/orders", methods=["GET"])
def api_list_orders():
    status = request.args.get("status")
    q = Order.query
    if status:
        q = q.filter_by(status=status)
    orders = q.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])


@app.route("/api/orders", methods=["POST"])
def api_create_order():
    data = request.get_json(force=True)
    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"error": "product not found"}), 404
    if product.stock < int(data.get("quantity", 1)):
        return jsonify({"error": "insufficient stock"}), 400

    order = Order(
        customer_name=data["customer_name"],
        product_id=product.id,
        quantity=int(data.get("quantity", 1)),
        status="pending",
    )
    product.stock -= order.quantity
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201


@app.route("/api/orders/<int:order_id>", methods=["GET"])
def api_get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())


@app.route("/api/orders/<int:order_id>", methods=["PUT"])
def api_update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json(force=True)
    if "status" in data:
        order.status = data["status"]
    db.session.commit()
    return jsonify(order.to_dict())


@app.route("/api/orders/<int:order_id>", methods=["DELETE"])
def api_delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"deleted": order_id})


# --------------------------------------------------------------- AUTH ------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# -------------------------------------------------------- ADMIN DASHBOARD --
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    products = Product.query.all()
    stats = {
        "total_orders": len(orders),
        "pending": sum(1 for o in orders if o.status == "pending"),
        "shipped": sum(1 for o in orders if o.status == "shipped"),
        "revenue": sum((o.product.price if o.product else 0) * o.quantity for o in orders),
    }
    return render_template("dashboard.html", orders=orders, products=products, stats=stats)


@app.route("/dashboard/orders/<int:order_id>/status", methods=["POST"])
@login_required
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("dashboard"))


# ------------------------------------------------------------- SEED DATA ---
def seed_database():
    db.create_all()
    if User.query.count() == 0:
        admin = User(username="admin")
        admin.set_password("orderflow2026")
        db.session.add(admin)

    if Product.query.count() == 0:
        demo_products = [
            Product(name="Hydraulic Seal Kit — Standard", sku="SEAL-STD-01", price=1450.0, stock=40),
            Product(name="Pneumatic O-Ring Set", sku="ORING-PN-02", price=380.0, stock=120),
            Product(name="CNC Spindle Wiper Seal", sku="WIPER-CNC-03", price=920.0, stock=25),
        ]
        db.session.add_all(demo_products)

    db.session.commit()

    if Order.query.count() == 0:
        p1 = Product.query.first()
        demo_orders = [
            Order(customer_name="Anand Textiles Pvt Ltd", product_id=p1.id, quantity=4, status="processing"),
            Order(customer_name="Vetri Precision Works", product_id=p1.id, quantity=2, status="pending"),
        ]
        db.session.add_all(demo_orders)
        db.session.commit()


with app.app_context():
    seed_database()


if __name__ == "__main__":
    app.run(debug=True)
