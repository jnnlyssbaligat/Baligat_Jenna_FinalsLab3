# Step-by-Step Guide: Members-Only Lounge Dashboard (Week 15)

A **separate project** from Weeks 13 and 14. It uses Django's built-in `User` model, `authenticate()`,
`login()`, `logout()` and `@login_required` with your own login template. 12 tests pass.

---

## Part 1 — Set up the project folder

```
lounge_project/
├── manage.py
├── requirements.txt
├── README.md  GUIDE.md  PRIVACY_ACCESS_REFLECTION.md  .gitignore
├── config/        settings.py, urls.py, wsgi.py
├── lounge/        views.py, urls.py, tests.py
├── templates/     base.html, login.html, dashboard.html
└── static/css/    style.css
```

1. Make a **new** folder (e.g. `Baligat_Jenna_FinalsLab3`) and put the extracted project in it.
2. In VS Code, open a terminal in the folder that contains `manage.py` (run `dir` to check).
3. Install Django. Because your PC blocked `pip.exe` last time, always use `python -m pip`:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```
   (If the venv is blocked, reuse your Week 13 venv, it already has Django.)
4. Create the tables, which also creates the `auth_user` table: `python manage.py migrate`
5. **Create your test user (Step 2):** `python manage.py createsuperuser` and choose a username and password you will remember.
6. `python manage.py runserver`, then open http://127.0.0.1:8000/

> **Personalize it:** change the brand name "Heavenly Lounge" in `base.html`, the dashboard text and
> announcements in `views.py` and `dashboard.html`, or the colours in `style.css`. If you rename the
> brand, nothing in the tests depends on it.

---

## Part 2 — Map the task steps to the code

| Step in the sheet | Where it lives |
|---|---|
| 1. `django.contrib.auth` installed | `config/settings.py` → `INSTALLED_APPS` (also `AuthenticationMiddleware` in `MIDDLEWARE`) |
| 2. Create a test user | `python manage.py createsuperuser` |
| 3. Login view: `authenticate()` then `login()` only if not `None` | `lounge/views.py` → `login_view` |
| 4. `@login_required` above the dashboard view | `lounge/views.py` → `dashboard` |
| 5. Your own login template | `templates/login.html` (POST form with `{% csrf_token %}`) |
| 6. `LOGIN_REDIRECT_URL` | `config/settings.py` (bottom), also `LOGIN_URL` and `LOGOUT_REDIRECT_URL` |
| 7. Working logout with its own view and redirect | `logout_view` in `views.py`; button in `base.html` |
| 8. Test logged out | See Part 3 |
| URLs | `lounge/urls.py` |

Why `LOGIN_URL = "login"`: it tells `@login_required` where to send signed-out visitors.

**Extras beyond the sheet (be ready to explain them):**
- A wrong login shows one generic error ("Invalid username or password"), so it doesn't reveal which part was wrong.
- After login, the user returns to the page they originally wanted (`?next=`), and only if that address is on the same site (stops open-redirect attacks).
- Logout works only on POST, with a CSRF token. Visiting `/logout/` in the address bar does **not** log you out.

---

## Part 3 — Test it (and capture screenshots)

**Step 8, logged out:** open a private window and visit http://127.0.0.1:8000/dashboard/. The address bar
should change to `/login/?next=/dashboard/` and **no dashboard content** appears.

Then run through this:
1. Wrong password gives a red error, with no session.
2. Correct login lands on `/dashboard/` with "Welcome, yourname".
3. Click **Log out**, which takes you to `/login/` with a "signed out" message.
4. Press the browser Back button or visit `/dashboard/` again. You're sent back to the login page.

Run `python manage.py test` for the automated version.

**Code screenshots (the sheet's required list):**
1. `lounge/views.py`, showing `login_view`, `@login_required` / `dashboard`, and `logout_view`
2. `lounge/urls.py`
3. `templates/login.html`
4. `templates/base.html` (logout form) or the dashboard template
5. `config/settings.py` bottom section (`LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`)

**Output screenshots (with the address bar visible):**
6. The login page
7. The redirect proof: logged out, visiting `/dashboard/` lands on `/login/?next=/dashboard/`
8. The protected dashboard after signing in
9. Optional: the wrong-password error, and the terminal showing the tests passing

Build the PDF as before (Word or Google Docs, title, name and date, **Code** and **Output** headings
with captions, export to PDF).

---

## Part 4 — GitHub

1. https://github.com/new → e.g. `Baligat_Jenna_FinalsLab3`, **Public**, no README/.gitignore.
2. In the folder with `manage.py`:
   ```powershell
   git init
   git add .
   git status
   git commit -m "Add Week 15 members-only lounge with Django authentication"
   git branch -M main
   git remote add origin https://github.com/jnnlyssbaligat/Baligat_Jenna_FinalsLab3.git
   git push -u origin main
   ```
3. `db.sqlite3` (it holds your password hash) must **not** be in the repo. `.gitignore` already excludes it, so check `git status` anyway.

---

## Part 5 — Privacy & Access Reflection

A draft is in `PRIVACY_ACCESS_REFLECTION.md`. Your instructor's template wasn't in the PDF, so copy
the answers into theirs and put them in your own words. Use your own experience from testing.

---

## Submission checklist

- [ ] Project zip or GitHub link (−25 pts if missing)
- [ ] PDF of screenshots: code and output (−15 pts if missing)
- [ ] Completed Privacy & Access Reflection
- [ ] Submitted before the end of the lab session

## Troubleshooting

| Problem | Fix |
|---|---|
| `pip.exe` blocked | Use `python -m pip ...` |
| `no such table: auth_user` | Run `python manage.py migrate` |
| Login always says invalid | Check the username and password; create the user with `createsuperuser` first |
| 403 CSRF error | `{% csrf_token %}` missing inside the `<form>` |
| Dashboard shows without login | `@login_required` must be directly above `def dashboard` |
| Redirects to `/accounts/login/` and a 404 | `LOGIN_URL = "login"` is missing in settings |
| Clicking Log out does nothing visible | Use the **Log out button**, since typing `/logout/` only redirects |
