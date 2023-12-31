from django import forms
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class TransactionAddForm(forms.Form):
    """ Formular for adding a Transaction. """
    sell = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        "id":"sell"
        
    }), initial= False, required= False)

    amount = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "amount",
        "class": "form-control",
        "step": "any",
        "min-value": "0",

    }))
    date = forms.DateField(widget=DateInput(attrs={
        "id": "date",
        "class": "form-control",
    }
    ))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "price",
        "class": "form-control",
        "step": "0.01",
        "min-value": "0"
    }))
    tax = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "tax",
        "class": "form-control",
        "step": "any",
        "min-value": "0"
    }))
    charge = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "charge",
        "class": "form-control",
        "step": "any",
        "min-value": "0"
    }))
    post = forms.BooleanField(widget= forms.CheckboxInput(attrs={
        "id": "post"
    }), initial= False, required= False)
    postText = forms.CharField(widget=forms.Textarea(attrs={
        "id": "postText",
        "class": "form-control"
    }), max_length=1000, required=False)
    tags = forms.CharField(widget=forms.TextInput(attrs={
        "id": "tags",
        "class": "form-control"
    }), max_length=100, required=False)


class TransactionUpdateForm(forms.Form):
    """ Formular for updating an existing Transaction. """

    amount = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "amount",
        "class": "form-control",
        "step": "any",
        "min-value": "0",

    }))
    date = forms.DateField(widget=DateInput(attrs={
        "id": "date",
        "class": "form-control",
    }
    ))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "price",
        "class": "form-control",
        "step": "0.01",
        "min-value": "0"
    }))
    tax = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "tax",
        "class": "form-control",
        "step": "any",
        "min-value": "0"
    }))
    charge = forms.DecimalField(widget=forms.NumberInput(attrs={
        "id": "charge",
        "class": "form-control",
        "step": "any",
        "min-value": "0"
    }))
