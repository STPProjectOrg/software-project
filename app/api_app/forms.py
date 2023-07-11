from django import forms
import datetime
from .databaseservice import get_asset_choices

asset_choices = get_asset_choices()
currency_choices = [("USD","USD"), ("EUR","EUR"), ("GBP","GBP"), ("JPY","JPY"), ("KRW","KRW")]


class AddAssetData(forms.Form):
    asset = forms.CharField(label="Asset",widget=forms.Select(choices=asset_choices), initial="EUR", required=True)
    currency = forms.CharField(label="Currency",widget=forms.Select(choices=currency_choices), initial="EUR", required=True)
    dateFrom = forms.DateField(widget = forms.widgets.DateInput(attrs={'type': 'date', 'value': datetime.date.today()}), required=True)
    dateTo = forms.DateField(widget = forms.widgets.DateInput(attrs={'type': 'date', 'value': datetime.date.today()}),required=True)
