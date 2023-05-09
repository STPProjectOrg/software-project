from django import forms
from datetime import datetime
#from api_app.views import getAllCoinsFromDatabase

class DateInput(forms.DateInput):
    input_type = 'date'

class MyForm(forms.Form):
    #assets = getAllCoinsFromDatabase()
    assetChoices = []
    #for asset in assets:
    #    assetChoices.append((asset.name, asset.coinName))
    user = forms.CharField(max_length=20)
    assetDropdown = forms.CharField(label='Asset', widget=forms.Select(choices=assetChoices))
    amount = forms.FloatField()
    purchaseDate = forms.DateField(widget=DateInput, initial=datetime.now)
