from django import forms

class AddParticipantForm(forms.Form):
    participant = forms.CharField(max_length=10)

class AddMessageForm(forms.Form):
    message = forms.CharField(max_length=200)

