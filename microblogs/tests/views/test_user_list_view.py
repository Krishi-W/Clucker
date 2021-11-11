from django.test import TestCase
from django.urls import reverse

from microblogs.models import User

class UserListViewTestCase(TestCase):
    fixtures = ["microblogs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("user_list")

    def test_user_list_url(self):
        self.assertEqual(self.url, "/users/")

    def test_get_user_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_list.html")
        self.assertEqual(set(response.context["users"]), set(User.objects.all()))
        return response

    def test_all_users_in_database_are_listed(self):
        response = self.test_get_user_list()
        self.assertEqual(set(response.context["users"]), set(User.objects.all()))
        self._setUpUser()
        response = self.test_get_user_list()
        self.assertEqual(set(response.context["users"]), set(User.objects.all()))

    def _setUpUser(self):
        User.objects.get(username="@johndoe")
