from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AuthFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="member1", password="S3cure-pass-123")

    def test_logged_out_dashboard_redirects_to_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, "/login/?next=/dashboard/")

    def test_logged_out_visitor_never_sees_dashboard_content(self):
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertNotContains(response, "Lounge announcements")
        self.assertTemplateUsed(response, "login.html")

    def test_login_page_has_csrf_token_and_fields(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_valid_login_starts_session_and_lands_on_dashboard(self):
        response = self.client.post(
            reverse("login"), {"username": "member1", "password": "S3cure-pass-123"}
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertContains(self.client.get(reverse("dashboard")), "Welcome, member1")

    def test_wrong_password_shows_error_and_no_session(self):
        response = self.client.post(reverse("login"), {"username": "member1", "password": "nope"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unknown_user_gets_same_generic_error(self):
        response = self.client.post(reverse("login"), {"username": "ghost", "password": "x"})
        self.assertContains(response, "Invalid username or password")

    def test_login_redirects_back_to_next(self):
        response = self.client.post(
            reverse("login"),
            {"username": "member1", "password": "S3cure-pass-123", "next": "/dashboard/"},
        )
        self.assertRedirects(response, "/dashboard/")

    def test_login_ignores_external_next_url(self):
        response = self.client.post(
            reverse("login"),
            {"username": "member1", "password": "S3cure-pass-123", "next": "https://evil.example/"},
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_logout_post_ends_session_and_redirects_to_login(self):
        self.client.login(username="member1", password="S3cure-pass-123")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertRedirects(self.client.get(reverse("dashboard")), "/login/?next=/dashboard/")

    def test_logout_get_does_not_log_out(self):
        self.client.login(username="member1", password="S3cure-pass-123")
        self.client.get(reverse("logout"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_post_without_csrf_token_is_forbidden(self):
        strict = Client(enforce_csrf_checks=True)
        response = strict.post(reverse("login"), {"username": "member1", "password": "S3cure-pass-123"})
        self.assertEqual(response.status_code, 403)

    def test_signed_in_user_skips_login_page(self):
        self.client.login(username="member1", password="S3cure-pass-123")
        self.assertRedirects(self.client.get(reverse("login")), reverse("dashboard"))
