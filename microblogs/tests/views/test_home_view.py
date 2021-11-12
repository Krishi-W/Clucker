from django.test import TestCase
from django.urls import reverse

from microblogs.models import User

class HomeViewTestCase(TestCase):
    fixtures = ["microblogs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.url = reverse("home")

    def test_home_url(self):
        self.assertEqual(self.url, "/")

    def test_get_home_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("feed")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "feed.html")

    def test_get_home(self):
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, "home.html")
