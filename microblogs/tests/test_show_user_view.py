from django.test import TestCase
from django.urls import reverse

from microblogs.models import User

class ShowUserViewTestCase(TestCase):
    def setUp(self):
        self.user = self._setUpUser()
        self.url = reverse("show_user", kwargs={"user_id": 1})
        self.url2 = reverse("show_user", kwargs={"user_id": 2})

    def test_show_user_url(self):
        self.assertEqual(self.url, "/user/1")
        self.assertEqual(self.url2, "/user/2")

    def test_get_show_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_user.html")

    def test_correct_user_is_returned(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["user"], self.user)

    def test_case_when_id_is_incorrect(self):
        response = self.client.get(self.url2)
        self.assertIsNone(response.context["user"])

    def _setUpUser(self):
        user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog',
            is_active=True
        )
        user.save()
        return user
