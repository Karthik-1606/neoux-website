# ClientDesk — Django demo

A client portal: authenticated clients see their projects, status, progress and
documents; staff manage everything through the Django admin (acting as the CMS).
Built for Neoux Industrial Solutions to demonstrate Python/Django capability.

## Run locally
```
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Open http://127.0.0.1:8000

**Demo client login:** username `client1` · password `clientdesk2026`
**Staff / CMS admin:** http://127.0.0.1:8000/admin/ — username `admin` · password `clientdesk2026`

## What it demonstrates
- Django auth (login/logout) scoped so clients only see their own data
- Models: Client, Project, ProjectUpdate, Document (file uploads)
- Django admin used as a real CMS — staff add projects, post updates, upload docs
  and clients see it live on their dashboard, no redeploy needed
- Progress bars, status badges, per-project detail pages

## Deploy for free (to get a real live link) — Render.com
1. Push this folder to a GitHub repo.
2. Go to https://render.com → New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_demo && python manage.py collectstatic --noinput`
4. Start command: `gunicorn clientdesk.wsgi`
5. Add environment variable `DJANGO_ALLOWED_HOSTS` if you lock down `ALLOWED_HOSTS` for production (currently set to `*` for demo convenience — tighten this before using with real client data).
6. Deploy. Render gives you a URL like `https://clientdesk-demo.onrender.com`.

(Railway.app and PythonAnywhere work the same way if you prefer those.)
