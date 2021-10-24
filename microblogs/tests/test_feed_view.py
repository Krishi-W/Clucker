from django.test import TestCase
from django.urls import reverse

from microblogs.forms import PostForm

class FeedViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("feed")

    def test_feed_url(self):
        self.assertEqual(self.url, "/feed/")

    def test_get_feed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feed.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)
