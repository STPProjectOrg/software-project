from django import forms

class AddMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=1000)

