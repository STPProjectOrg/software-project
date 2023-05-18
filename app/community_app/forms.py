from django import forms

class PostForm(forms.Form):
    asset = forms.CharField(max_length=10)
    content = forms.CharField(widget=forms.Textarea, max_length=1000)
    hashtags = forms.CharField(max_length=100)

