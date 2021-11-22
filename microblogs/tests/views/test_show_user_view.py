from django.test import TestCase
from django.urls import reverse

from microblogs.models import User
from microblogs.tests.helpers import reverse_with_next, create_posts

class ShowUserViewTestCase(TestCase):
    fixtures = [
        "microblogs/tests/fixtures/default_user.json",
        "microblogs/tests/fixtures/other_default_user.json"
    ]

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
        response = self.client.get(self.url2, follow=True)
        redirect_url = reverse("user_list")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_show_user_displays_posts_belonging_to_the_shown_user_only(self):
        self.client.login(username=self.user.username, password="Password123")
        other_user = User.objects.get(username="@janedoe")
        create_posts(other_user, 100, 103)
        create_posts(self.user, 200, 203)
        url = reverse("show_user", kwargs={"user_id": other_user.id})
        response = self.client.get(url)
        for count in range(100, 103):
            self.assertContains(response, f"Post_{count}")
        for count in range(200, 203):
            self.assertNotContains(response, f"Post_{count}")
