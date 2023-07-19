from django import forms


class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "id": "content",
        "class": "form-control",
        "placeholder": "Text eingeben ...",
        "rows": "5"
    }), max_length=1000)
    tags = forms.CharField(widget=forms.TextInput(attrs={
        "id": "tags",
        "class": "form-control"
    }), max_length=100, required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'id': "image_To_Upload",
        "class": "form-control"
    }), required=False)
