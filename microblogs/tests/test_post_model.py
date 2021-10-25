from django.test import TestCase
from django.core.exceptions import ValidationError

from microblogs.models import User
from microblogs.models import Post

class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog'
        )

        self.post = Post(
            author=self.user,
            text="The first ever cluck!"
        )

    def test_valid_post(self):
        self._assert_post_is_valid()

    def test_post_is_deleted_if_author_is_deleted(self):
        self.user.delete()
        self._assert_post_is_invalid()

    def test_multiple_posts_can_have_same_author(self):
        post = self._create_second_post()
        self.post.author = post.author
        self._assert_post_is_valid

    def test_author_cannot_be_blank(self):
        self.post.author = None
        self._assert_post_is_invalid

    def test_text_has_length_no_longer_than_280_chars(self):
        self.post.text = "x" * 281
        self._assert_post_is_invalid

    def test_text_is_not_blank(self):
        self.post.text = ""
        self._assert_post_is_invalid

    def test_text_may_already_exist(self):
        post = self._create_second_post()
        self.post.text = post.text
        self._assert_post_is_valid

    def _assert_post_is_valid(self):
        try:
            self.post.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_post_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def _create_second_user(self):
        user = User.objects.create_user(
            '@janedoe',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.org',
            password='Password123',
            bio='This is Jane\'s profile.'
        )

        return user

    def _create_second_post(self):
        user = self._create_second_user()

        post = Post(
            author=user,
            text="The second ever cluck!"
        )

        return post