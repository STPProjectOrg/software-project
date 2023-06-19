from django.test import SimpleTestCase
from community_app.forms import PostForm

class TestForms(SimpleTestCase):

    # PostForm
    def test_post_form_valid_data(self):
        form = PostForm(data={
            'content': 'Test Post Form',
            'tags': 'TestTag',
            'image': ''
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["content"], "Test Post Form")
        self.assertEqual(form.data["tags"], "TestTag")
        self.assertEqual(form.data["image"], "")

    def test_post_form_no_data(self):
        form = PostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)