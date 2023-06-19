from django import forms
from datetime import datetime
from api_app.views import getAllCoinsFromDatabase


class DateInput(forms.DateInput):
    input_type = 'date'


class AddToPortfolioForm(forms.Form):
    assets = getAllCoinsFromDatabase()
    assetChoices = []
    for asset in assets:
        assetChoices.append((asset.name, asset.coinName))
    user = forms.CharField(max_length=20)
    assetDropdown = forms.CharField(
        label='Asset', widget=forms.Select(choices=assetChoices))
    amount = forms.FloatField()
    purchaseDate = forms.DateField(widget=DateInput, initial=datetime.now)


class AddToPortfolioForm2(forms.Form):
    user = forms.CharField(max_length=20)
    user.widget = user.hidden_widget()
    assetDropdown = forms.CharField(max_length=20)
    assetDropdown.widget = assetDropdown.hidden_widget()
    amount = forms.FloatField()
    purchaseDate = forms.DateField(widget=DateInput, initial=datetime.now)


class TransactionBuyForm(forms.Form):
    """ Formular for adding a Buy-Transaction. """

    amount = forms.FloatField()
    date = forms.DateField(widget=DateInput, initial=datetime.now)
    price = forms.FloatField(initial=0)
    tax = forms.FloatField(initial=0)
    charge = forms.FloatField(initial=0)
    post = forms.BooleanField(required=False)
    postText = forms.CharField(widget=forms.Textarea, max_length=1000, required=False)
    tags = forms.CharField(max_length=100, required=False)
