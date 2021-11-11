from django.test import TestCase
from django.core.exceptions import ValidationError

from microblogs.models import User

class UserModelTestCase(TestCase):
    fixtures = [
        "microblogs/tests/fixtures/default_user.json",
        "microblogs/tests/fixtures/other_default_user.json"
    ]

    def setUp(self):
        self.userJohn = User.objects.get(username="@johndoe")
        self.userJane = User.objects.get(username="@janedoe")

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.userJohn.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.userJohn.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_longer_than_30_characters(self):
        self.userJohn.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        self.userJohn.username = self.userJane.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_the_at_symbol(self):
        self.userJohn.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.userJohn.username = '@!johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.userJohn.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.userJohn.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.userJohn.username = '@@j0hndoe2'
        self._assert_user_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.userJohn.first_name = ""
        self._assert_user_is_invalid()

    def test_first_name_may_already_exist(self):
        self.userJohn.first_name = self.userJane.first_name
        self._assert_user_is_valid()

    def test_first_name_has_maximum_fifty_characters(self):
        self.userJohn.first_name = "x" * 51
        self._assert_user_is_invalid()

    def test_last_name_must_not_be_blank(self):
        self.userJohn.last_name = ""
        self._assert_user_is_invalid()

    def test_last_name_may_already_exist(self):
        self.userJohn.last_name = self.userJane.last_name

        self._assert_user_is_valid()

    def test_last_name_has_maximum_fifty_characters(self):
        self.userJohn.last_name = "x" * 51
        self._assert_user_is_invalid()

    def test_email_is_unique(self):
        self.userJohn.email = self.userJane.email
        self._assert_user_is_invalid()

    def test_email_is_must_not_be_blank(self):
        self.userJohn.email = ""
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.userJohn.email = "@example.org"
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.userJohn.email = "johndoe.example.org"
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.userJohn.email = "johndoe@.org"
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.userJohn.email = "johndoe@example"
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.userJohn.email = "johndoe@@example.org"
        self._assert_user_is_invalid()

    def test_bio_may_be_blank(self):
        self.userJohn.bio = ""
        self._assert_user_is_valid()

    def test_bio_may_already_exist(self):
        self.userJohn.bio = self.userJane.bio
        self._assert_user_is_valid()

    def test_bio_has_length_no_longer_than_520_characters(self):
        self.userJohn.bio = "x" * 521
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.userJohn.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.userJohn.full_clean()
