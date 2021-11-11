from django.test import TestCase
from django.urls import reverse

from microblogs.models import User
from microblogs.tests.helpers import reverse_with_next

class UserListViewTestCase(TestCase):
    fixtures = ["microblogs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("user_list")

    def test_user_list_url(self):
        self.assertEqual(self.url, "/users/")

    def test_get_user_list(self):
        self.client.login(username="@johndoe", password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_list.html")
        self.assertEqual(set(response.context["users"]), set(User.objects.all()))
        return response

    def test_get_user_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_all_users_in_database_are_listed(self):
        response = self.test_get_user_list()
        self.assertEqual(set(response.context["users"]), set(User.objects.all()))
        self._setUpUser()
        response = self.test_get_user_list()
        self.assertEqual(set(response.context["users"]), set(User.objects.all()))

    def _setUpUser(self):
        User.objects.get(username="@johndoe")
