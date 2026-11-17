from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

ANNOUNCEMENTS = [
    {"title": "Weekly Members' Mixer", "detail": "Every Friday, 6:00 PM in the main lounge."},
    {"title": "New Study Room Booking", "detail": "Reserve a quiet room up to 7 days ahead."},
    {"title": "Member Perks Refreshed", "detail": "Check the perks list for this month's offers."},
]


def home(request):
    """Send visitors to the right place: dashboard if signed in, login if not."""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def login_view(request):
    # Already signed in? No need to show the form again.
    if request.user.is_authenticated:
        return redirect("dashboard")

    error = None
    if request.method == "POST":
        uname = request.POST.get("username", "").strip()
        pwd = request.POST.get("password", "")

        # authenticate() checks the credentials and returns a User or None.
        # It does NOT start a session by itself.
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            # login() is the line that starts the session and sets the cookie.
            login(request, user)

            # If @login_required sent the user here, return them to where they were
            # heading, but only if that address is safe (same site).
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect(settings.LOGIN_REDIRECT_URL)

        # One generic message: don't reveal whether the username or the password was wrong.
        error = "Invalid username or password. Please try again."

    return render(
        request,
        "login.html",
        {"error": error, "next": request.GET.get("next", "")},
    )


@login_required
def dashboard(request):
    # The function body never runs for a signed-out visitor: Django redirects to LOGIN_URL first.
    context = {"announcements": ANNOUNCEMENTS}
    return render(request, "dashboard.html", context)


def logout_view(request):
    # Logging out changes state, so it only happens on POST (protected by the CSRF token
    # in the dashboard's logout button). A plain GET just redirects.
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been signed out.")
        return redirect("login")
    return redirect("dashboard")

