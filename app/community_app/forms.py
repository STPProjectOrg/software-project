from django import forms
from datetime import datetime

class PostForm(forms.Form):
    user_id = forms.CharField(max_length=10)
    user_id = user_id.hidden_widget
    asset = forms.CharField(max_length=10)
    #asset = asset.hidden_widget
    content = forms.CharField(widget=forms.Textarea, max_length=1000)
    created_at = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.now)
    #created_at.widget = created_at.hidden_widget
    hashtags = forms.CharField(max_length=100)

