from django import forms
import datetime
from .databaseservice import get_asset_choices

currency_choices = [('USD','USD'),
                    ('EUR','EUR'), 
                    ('GBP','GBP'), 
                    ('JPY','JPY'), 
                    ('KRW','KRW')]


class AddAssetDataForm(forms.Form):
    asset = forms.CharField(label='Cryptocoin Symbol',
                            initial='EUR',
                            required=True,
                            widget=forms.Select(
                                choices=get_asset_choices(), 
                                attrs={'class': 'form-control'}))
    
    currency = forms.CharField(label='Währung',
                               initial='EUR', 
                               required=True,
                               widget=forms.Select(
                                   choices=currency_choices, 
                                   attrs={'class': 'form-control'}))
    
    dateFrom = forms.DateField(label='Von:', 
                               required=True,
                               widget = forms.widgets.DateInput(
                                   attrs={
                                        'type': 'date', 
                                        'class': 'form-control',
                                        'value': datetime.date.today()
                                        }))
    
    dateTo = forms.DateField(label='Bis:', 
                             required=True,
                             widget = forms.widgets.DateInput(
                                 attrs={
                                     'type': 'date', 
                                     'class': 'form-control',
                                     'value': datetime.date.today()
                                     }))

class AddCoinForm(forms.Form):
    asset = forms.CharField(label='Cryptocoin Symbol',
                            required=True,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control'
                                    }))
    
    currency = forms.CharField(label='Währung',
                               initial='EUR', 
                               required=True,
                               widget=forms.Select(
                                   choices=currency_choices, 
                                   attrs={
                                       'class': 'form-control'
                                       }))