from django import forms

class AddMessageForm(forms.Form):
    message = forms.CharField(max_length=200)

