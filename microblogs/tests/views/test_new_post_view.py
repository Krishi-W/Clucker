from django.test import TestCase
from django.urls import reverse

from microblogs.models import Post, User

class NewPostViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("new_post")
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog',
            is_active=True
        )
        self.user.save()

    def test_new_post_url(self):
        self.assertEqual(self.url, "/new_post/")

    def test_new_post_with_invalid_form_but_logged_in(self):
        self._login_user()
        form_input = {
            "text": ""
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

    def test_new_post_with_invalid_form_and_not_logged_in(self):
        form_input = {
            "text": ""
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

    def test_new_post_with_vaild_form_but_not_logged_in(self):
        form_input = {
            "text": "Valid text"
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

    def test_new_post_with_valid_form_and_logged_in(self):
        self._login_user()
        form_input = {
            "text": "Valid text"
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertRedirects(response, reverse("feed"), status_code=302, target_status_code=200)

    def test_a_valid_post_is_successfully_created(self):
        self._login_user()
        form_input = {
            "text": "Valid text"
        }
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(author_id=self.user.id)
        self.client.post(self.url, form_input, follow=True)
        post = Post.objects.get(author_id=self.user.id)
        self.assertEqual("Valid text", post.text)

    def _login_user(self):
        form_input = {
            "username": "@johndoe",
            "password": "Password123"
        }
        self.client.post(reverse("log_in"), form_input, follow=True)