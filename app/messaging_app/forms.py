from django import forms
from PIL import Image

class AddMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control chat-textarea',
        'placeholder': 'Gib eine Nachricht ein...',
        'rows': '2',
    }),
        max_length=1000)
    image = forms.ImageField(required=False)