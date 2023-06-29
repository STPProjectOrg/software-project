from django import forms


class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, max_length=1000)
    tags = forms.CharField(max_length=100, required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'id': "image_To_Upload",
    }) ,required=False)

