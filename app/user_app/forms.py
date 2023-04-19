from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from user_app.models import UserProfileInfo
from .models import CustomUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = CustomUser 
        fields = ('first_name','last_name','username','email','password')

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
            msg = "Password does not match! Try again"
            self.add_error("password2", msg)
        self.set_form_control()


        '''
            if hasattr(self, 'cleaned_data') and field_name in self.cleaned_data and self.cleaned_data[field_name]:
                if field_name in self.errors:
                    field.widget.attrs['class'] = 'form-control is-invalid'
                else:
                    field.widget.attrs['class'] = 'form-control is-valid'
            else:
                field.widget.attrs['class'] = 'form-control'


            
            if field_name in self.errors:
                field.widget.attrs['class'] = 'form-control is-invalid'
            elif field_name in self.fields:
                field.widget.attrs['class'] = 'form-control is-valid'
            else:
                field.widget.attrs['class'] = 'form-control'
            '''

    

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password'
    }))