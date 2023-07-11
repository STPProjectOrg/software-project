from django import forms
import datetime
from .databaseservice import get_asset_choices

asset_choices = get_asset_choices()
currency_choices = [("USD","USD"), ("EUR","EUR"), ("GBP","GBP"), ("JPY","JPY"), ("KRW","KRW")]


class AddAssetData(forms.Form):
    asset = forms.CharField(label="Cryptocoin Symbol",widget=forms.Select(choices=asset_choices, attrs={"class": "form-control"}), initial="EUR", required=True)
    currency = forms.CharField(label="Währung",widget=forms.Select(choices=currency_choices, attrs={"class": "form-control"}), initial="EUR", required=True)
    dateFrom = forms.DateField(label="Von:", widget = forms.widgets.DateInput(attrs={'type': 'date', "class": "form-control",'value': datetime.date.today()}), required=True)
    dateTo = forms.DateField(label="Bis:", widget = forms.widgets.DateInput(attrs={'type': 'date', "class": "form-control",'value': datetime.date.today()}),required=True)

class AddCoin(forms.Form):
    asset = forms.CharField(label="Cryptocoin Symbol",widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    currency = forms.CharField(label="Währung",widget=forms.Select(choices=currency_choices, attrs={"class": "form-control"}), initial="EUR", required=True)