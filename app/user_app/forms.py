from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from user_app.models import UserProfileInfo
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control bg-body-secondary',
        'placeholder': 'Benutzername',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control bg-body-tertiary border-start-0',
        'placeholder': 'Passwort',
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password2',
        'class': 'form-control bg-body-tertiary border-start-0',
        'placeholder': 'Passwort',
    }))
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'first_name',
        'class': 'form-control bg-body-tertiary border-start-0',
        'placeholder': 'Vorname',
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'last_name',
        'class': 'form-control bg-body-tertiary border-start-0',
        'placeholder': 'Nachname',
    }))
    
    email = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'email',
        'class': 'form-control bg-body-tertiary border-start-0',
        'placeholder': 'E-Mail',
    }))

    class Meta():
        model = CustomUser 
        fields = ('first_name','last_name','username','email','password')

    def set_form_control(self):
        for field_name, field in self.fields.items():
            if self.is_bound:
                if field_name in self.errors:
                    field.widget.attrs['class'] = 'form-control bg-body-tertiary is-invalid'
                else:
                    field.widget.attrs['class'] = 'form-control bg-body-tertiary is-valid' 
            else:
                field.widget.attrs['class'] = 'form-control bg-body-tertiary border-start-0'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            msg = "Password does not match! Try again"
            self.add_error("password2", msg)
        self.set_form_control()


    

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control bg-body-tertiary border-start-0',
        'placeholder': 'Benutzername',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control bg-body-tertiary border-start-0',
        'placeholder': 'Passwort'
    }))