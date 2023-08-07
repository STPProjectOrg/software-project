from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser

invalid_email_msg = 'Email ist bereits vergeben oder falsch.'
invalid_login_msg = 'Bitte geben Sie einen korrekten Benutzernamen und ein korrektes Passwort ein. Bedenke, dass möglicherweise Groß-und Kleinschreibung in beiden Feldern beachtet werden muss.'
invalid_password_match_msg = "Passwörter stimmen nicht überein! Versuchs nochmal."
invalid_username_msg = "Benutzername ist bereits vergeben!"


class UserRegistrationForm(forms.ModelForm):
    """
    ModelForm for user registration.

    This form is used to handle user registration data input. It includes fields for username,
    password, password confirmation, first name, last name, and email. The form provides custom
    widgets and placeholder text for each field.

    Attributes:
        username (CharField): Field for the username input.
        password (CharField): Field for the password input.
        password2 (CharField): Field for the password confirmation input.
        first_name (CharField): Field for the user's first name input.
        last_name (CharField): Field for the user's last name input.
        email (CharField): Field for the user's email input.

    Methods:
        set_form_control(): Sets the appropriate CSS class for each form field based on its validity.
        clean(self): Custom form validation for password matching.

    Meta:
        model (CustomUser): The model associated with the form.
        fields (tuple): The fields to be included in the form.
    """
    # Form fields with custom widget attributes
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control',
        'placeholder': 'Benutzername',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Passwort',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password2',
        'class': 'form-control',
        'placeholder': 'Passwort',
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'first_name',
        'class': 'form-control',
        'placeholder': 'Vorname',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'last_name',
        'class': 'form-control',
        'placeholder': 'Nachname',
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'email',
        'class': 'form-control',
        'placeholder': 'E-Mail',
    }), error_messages={'invalid': invalid_email_msg})

    class Meta():
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def set_form_control(self):
        for field_name, field in self.fields.items():
            if self.is_bound:
                if field_name in self.errors:
                    field.widget.attrs['class'] = 'form-control is-invalid'
                else:
                    field.widget.attrs['class'] = 'form-control is-valid'
            else:
                field.widget.attrs['class'] = 'form-control'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", invalid_password_match_msg)
        self.set_form_control()


class UserLoginForm(AuthenticationForm):
    """
    Custom login form for user authentication. This class represents 
    a custom login form that inherits from Django's built-in AuthenticationForm.
    It provides additional customization to the form fields, 
    such as widget attributes.

    Attributes:
        username (CharField): A field to capture the user's username.
        password (CharField): A field to capture the user's password.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control',
        'placeholder': 'Benutzername',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Passwort'
    }))

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = invalid_login_msg
        super().__init__(*args, **kwargs)


class PasswordCustomResetForm(PasswordResetForm):
     """
    Custom password reset form for resetting user passwords.
    This class represents a custom password reset form that inherits 
    from Django's built-in PasswordResetForm.

    Attributes:
        email (EmailField): A field to capture the user's email address for password reset. 
            The field is also marked as required, ensuring that the user must provide an 
            email address for the password reset request.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'id_email',
        'class': 'form-control',
        'placeholder': 'E-Mail'
    }), required=True)


class PasswordCustomSetForm(SetPasswordForm):
     """
    Custom password set form for setting a new user password.
    This class represents a custom password set form that inherits 
    from Django's built-in SetPasswordForm.

    Attributes:
        new_password1 (CharField): A field to capture the user's new password. 
            The field is also marked as required, ensuring that the user must 
            provide a new password.

        new_password2 (CharField): A field to confirm the user's new password. 
            The field is also marked as required, ensuring that the user must 
            confirm the new password by entering it again.
    """
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'id_new_password1',
        'class': 'form-control',
        'placeholder': 'Passwort',
    }), required=True)

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'id_new_password2',
        'class': 'form-control',
        'placeholder': 'Passwort',
    }), required=True)
