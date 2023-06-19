from django.test import SimpleTestCase
from user_app.forms import UserRegistrationForm

class TestForms(SimpleTestCase):
    '''
    #UserRegistrationForm
    def test_user_registration_form_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'TestUser',
            'password': "Test?123",
            'password2': "Test?123",
            'first_name': "Test",
            'last_name': "Tester",
            'email': "test@test.de",
        })
        self.assertTrue(form.is_valid())
        #registration = form.save()
        #self.assertEqual(registration.username , "TestUser")
    '''

    def test_user_registration_form_no_data(self):
        form = UserRegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)