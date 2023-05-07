from django import forms
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = 'date'

class MyForm(forms.Form):
    user = forms.CharField(max_length=20)
    asset = forms.CharField(max_length=20)
    purchaseDate = forms.DateField(widget=DateInput, initial=datetime.now)
    purchaseValue = forms.CharField(max_length=20)