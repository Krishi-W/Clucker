from django.test import TestCase
from django.urls import reverse

from microblogs.forms import PostForm
from microblogs.models import Post, User
from microblogs.tests.helpers import reverse_with_next

class FeedViewTestCase(TestCase):
    fixtures = [
        "microblogs/tests/fixtures/default_user.json",
        "microblogs/tests/fixtures/other_default_user.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.url = reverse("feed")

    def test_feed_url(self):
        self.assertEqual(self.url, "/feed/")

    def test_get_feed(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feed.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_feed_displays_posts_belonging_to_the_logged_in_user_only(self):
        self.client.login(username=self.user.username, password="Password123")
        other_user = User.objects.get(username="@janedoe")
        create_posts(other_user, 100, 103)
        create_posts(self.user, 200, 203)
        response = self.client.get(self.url)
        for count in range(200, 203):
            self.assertContains(response, f"Post_{count}")
        for count in range(100, 103):
            self.assertNotContains(response, f"Post_{count}")

def create_posts(author, from_count, to_count):
    for count in range(from_count, to_count):
        text = f"Post_{count}"
        post = Post(author=author, text=text)
        post.save()
