# Heavenly Lounge (Django) — Week 15

A members-only dashboard protected by Django's authentication system.

## Run it

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (macOS/Linux: source venv/bin/activate)
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in. Run tests with `python manage.py test`.

## Structure

| Path | Purpose |
|------|---------|
| `lounge/views.py` | `login_view` (authenticate + login), `dashboard` (`@login_required`), `logout_view` |
| `lounge/urls.py` | `/login/`, `/dashboard/`, `/logout/` |
| `templates/` | `base.html`, `login.html`, `dashboard.html` |
| `config/settings.py` | `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` |

Course: PC15 Python Programming 2 w/ Lab — National Teachers College
