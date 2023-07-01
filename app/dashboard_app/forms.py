from django import forms
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionBuyForm(forms.Form):
    """ Formular for adding a Buy-Transaction. """

    amount = forms.FloatField()
    date = forms.DateField(widget=DateInput, initial=datetime.now)
    price = forms.FloatField(initial=0)
    tax = forms.FloatField(initial=0)
    charge = forms.FloatField(initial=0)
    post = forms.BooleanField(required=False)
    postText = forms.CharField(
        widget=forms.Textarea, max_length=1000, required=False)
    tags = forms.CharField(max_length=100, required=False)
