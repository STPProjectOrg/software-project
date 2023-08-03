from django.test import SimpleTestCase, TestCase
from user_app.forms import UserRegistrationForm

class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        """
        Test that the form is valid with valid data.
        """
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
        }

        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test that the form is invalid with invalid data.
        """
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'differentpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalidemail',
        }

        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('email', form.errors)

    def test_form_control_class(self):
        """
        Test that the form control class is correctly set based on field validity.
        """
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
        }

        form = UserRegistrationForm(data=form_data)
        form.is_valid()
        for field_name, field in form.fields.items():
            if field_name in form.errors:
                self.assertEqual(field.widget.attrs['class'], 'form-control is-invalid')
            else:
                self.assertEqual(field.widget.attrs['class'], 'form-control is-valid')