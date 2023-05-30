from django import forms


class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, max_length=1000)
    tags = forms.CharField(max_length=100)
