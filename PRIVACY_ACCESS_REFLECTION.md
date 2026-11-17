# Privacy & Access Reflection — Week 15: Members-Only Lounge Dashboard

**Name:** Jenna Baligat  **Course:** PC15 Python Programming 2 w/ Lab  **Date:** November 17, 2026

> Draft based on this project's code. Your instructor's reflection questions weren't in the assignment
> PDF, so adapt these answers to their template and rewrite them in your own words, adding what you
> observed while testing.

## 1. What did I build?

A lounge dashboard that only signed-in users can open. It uses Django's built-in `User` model,
`authenticate()` and `login()` to start a session, `@login_required` to guard the dashboard, a custom
login template, and a `logout()` view that ends the session.

## 2. How does access control work in my app?

- **Authentication:** `authenticate(request, username, password)` checks the credentials against the database. It returns a `User` or `None`, and it does not log anyone in by itself.
- **Session:** only inside `if user is not None:` do I call `login(request, user)`, which creates the session and sets the browser's session cookie.
- **Authorization:** `@login_required` on `dashboard` means a signed-out visitor is redirected to `LOGIN_URL` before any dashboard code runs. When I visited `/dashboard/` while signed out, I landed on `/login/?next=/dashboard/` and saw no content.
- **Ending access:** `logout(request)` clears the session, then redirects to the login page.

## 3. What user data does my app handle, and how is it protected?

| Data | Handling |
|---|---|
| Password | Never stored in plain text. Django stores a salted hash (PBKDF2) in the database, and `authenticate()` compares hashes. The app never displays or logs it. |
| Username | Shown on the dashboard to the signed-in user only. |
| Session ID | Stored in a cookie, with the session data kept server-side. Django's session cookie is `HttpOnly` by default, so page JavaScript can't read it. |
| Account dates | "Member since" shows the user's own `date_joined`. |

## 4. Security and privacy decisions I made

1. **Generic login error.** A failed login says "Invalid username or password" and doesn't say which was wrong, so attackers can't use it to find valid usernames.
2. **CSRF protection** on the login and logout forms (`{% csrf_token %}`).
3. **Logout only on POST.** A link or image on another site can't log a member out by making their browser load `/logout/`.
4. **Safe redirects.** After login, the `next` address is used only if it is on this same site, which prevents open-redirect phishing.
5. **Auto-escaped output.** Django templates escape usernames and text by default, which reduces XSS risk.
6. **No secrets in Git.** `db.sqlite3` (which holds password hashes) is listed in `.gitignore`.

## 5. Limitations and what I would add for a real deployment

- `DEBUG = True` and the placeholder `SECRET_KEY` are for development only. In production, set `DEBUG = False`, load the key from an environment variable, and set `ALLOWED_HOSTS`.
- Serve over **HTTPS** and enable `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE`.
- Add **rate limiting or lockout** for repeated failed logins (for example with django-axes) to slow brute-force guessing.
- Add **password reset**, optional **two-factor authentication**, and a session timeout.
- Collect only the data the app really needs (data-minimisation), and tell users what is stored and why.

## 6. Reflection

Signing in proves who someone is, and `@login_required` decides what they may see. Both are needed.
The part I could most easily have missed is calling `login()` after `authenticate()`, since
`authenticate()` alone doesn't create a session. Handling a user's password carefully, by hashing it,
never showing it, and giving vague errors, is a core part of earning users' trust, and it applies directly
to my final project's protected pages.
