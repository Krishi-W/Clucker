from django.test import TestCase
from django.urls import reverse

from microblogs.models import User
from microblogs.tests.helpers import reverse_with_next

class ShowUserViewTestCase(TestCase):
    fixtures = ["microblogs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.url = reverse("show_user", kwargs={"user_id": 1})
        self.url2 = reverse("show_user", kwargs={"user_id": 3})

    def test_show_user_url(self):
        self.assertEqual(self.url, "/user/1")
        self.assertEqual(self.url2, "/user/3")

    def test_get_show_user_with_valid_id(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_user.html")

    def test_correct_user_is_returned(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["user"], self.user)

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_case_when_id_is_incorrect(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url2)
        self.assertIsNone(response.context["user"])
