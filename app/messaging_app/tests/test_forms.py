from django.test import SimpleTestCase
from messaging_app.forms import AddMessageForm

class TestForms(SimpleTestCase):

    #AddMessageForm
    def test_add_message_form_valid_data(self):
        form = AddMessageForm(data={
            'message': 'Test Message',
            'image': "test.png"
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["message"], "Test Message")
        self.assertEqual(form.data["image"], "test.png")


    def test_add_message_form_no_data(self):
        form = AddMessageForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)