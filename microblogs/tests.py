from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User
from .models import Post

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog'
        )

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_longer_than_30_characters(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        user = self._create_second_user()

        self.user.username = user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_the_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@!johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@j0hndoe2'
        self._assert_user_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ""
        self._assert_user_is_invalid()

    def test_first_name_may_already_exist(self):
        user = self._create_second_user()
        self.user.first_name = user.first_name
        self._assert_user_is_valid()

    def test_first_name_has_maximum_fifty_characters(self):
        self.user.first_name = "x" * 51
        self._assert_user_is_invalid()

    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ""
        self._assert_user_is_invalid()

    def test_last_name_may_already_exist(self):
        user = self._create_second_user()
        self.user.last_name = user.last_name

        self._assert_user_is_valid()

    def test_last_name_has_maximum_fifty_characters(self):
        self.user.last_name = "x" * 51
        self._assert_user_is_invalid()

    def test_email_is_unique(self):
        user = self._create_second_user()
        self.user.email = user.email

        self._assert_user_is_invalid()

    def test_email_is_must_not_be_blank(self):
        self.user.email = ""
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = "@example.org"
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = "johndoe.example.org"
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = "johndoe@.org"
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = "johndoe@example"
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = "johndoe@@example.org"
        self._assert_user_is_invalid()

    def test_bio_may_be_blank(self):
        self.user.bio = ""
        self._assert_user_is_valid()

    def test_bio_may_already_exist(self):
        user = self._create_second_user()
        self.user.bio = user.bio
        self._assert_user_is_valid()

    def test_bio_has_length_no_longer_than_520_characters(self):
        self.user.bio = "x" * 521
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

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