from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from user_app.models import UserProfileInfo
from .models import CustomUser

invalid_email_msg = 'Email ist bereits vergeben oder falsch.'
invalid_login_msg = 'Bitte geben Sie einen korrekten Benutzernamen und ein korrektes Passwort ein. Bedenke, dass möglicherweise Groß-und Kleinschreibung in beiden Feldern beachtet werden muss.'
invalid_password_match_msg = "Passwörter stimmen nicht überein! Versuchs nochmal."
invalid_username_msg = "Benutzername ist bereits vergeben!"

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control',
        'placeholder': 'Bebebebe',
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
    }),error_messages={'invalid': invalid_email_msg})

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
        #username = cleaned_data.get("username")
        #if CustomUser.objects.filter(username = username).exists:
        #    self.add_error("username", "Benutzername existiert bereits.")
        if password and password2 and password != password2:
            self.add_error("password2", invalid_password_match_msg)
        self.set_form_control()


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)


class UserLoginForm(AuthenticationForm):
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
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'id_email',
        'class': 'form-control',
        'placeholder': 'E-Mail'
    }), required=True)


class PasswordCustomSetForm(SetPasswordForm):
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
