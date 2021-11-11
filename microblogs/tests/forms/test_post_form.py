from django.test import TestCase

from microblogs.forms import PostForm

class PostFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            "text": "This is the first Cluck!"
        }

    def test_valid_post_form(self):
        form = PostForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = PostForm()
        self.assertIn("text", form.fields)

    def test_form_uses_model_validation(self):
        form = PostForm(data=self.form_input)
        self.assertTrue(form.is_valid())

        self.form_input["text"] = "x" * 281
        form = PostForm(data=self.form_input)
        self.assertFalse(form.is_valid())

        self.form_input["text"] = ""
        form = PostForm(data=self.form_input)
        self.assertFalse(form.is_valid())