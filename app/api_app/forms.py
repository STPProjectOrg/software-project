from django import forms
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = 'date'

class MyForm(forms.Form):
    asset = forms.CharField(max_length=20, initial='BTC')
    currency = forms.CharField(max_length=20, initial='EUR')
    dateFrom = forms.DateField(widget=DateInput, initial=datetime.now)
    dateTo = forms.DateField(widget=DateInput, initial=datetime.now)