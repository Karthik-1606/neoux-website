# OrderFlow API — Flask demo

A working order-management backend: REST API + login-protected admin dashboard.
Built for Neoux Industrial Solutions to demonstrate Python/Flask capability.

## Run locally
```
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 — you'll be redirected to `/login`.

**Demo login:** username `admin` · password `orderflow2026`

## What it demonstrates
- REST API: `GET/POST /api/orders`, `GET/PUT/DELETE /api/orders/<id>`, `GET/POST /api/products`
- Flask-SQLAlchemy models (Order, Product, User) with relationships
- Flask-Login session auth on the admin dashboard
- Live order-status updates from the dashboard
- SQLite by default; switch to Postgres by setting `DATABASE_URL`

## Deploy for free (to get a real live link) — Render.com
1. Push this folder to a GitHub repo.
2. Go to https://render.com → New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy. Render gives you a URL like `https://orderflow-demo.onrender.com` — use that as the "View demo" link on the Neoux site.

(Railway.app and PythonAnywhere work the same way if you prefer those.)
