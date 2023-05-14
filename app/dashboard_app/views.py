from django.shortcuts import render
from dashboard_app.models import Portfolio
from datetime import datetime, date
from api_app.views import getAssetFromDatabase, doesCoinExistInDatabase, getCoinInformation, getCryptoValuesFromDatabase
from user_app.views import getUser
from dashboard_app.forms import MyForm, MyForm2

# Create your views here.
def dashboard(request):
    message = ""
    form = MyForm()
    if request.method=='POST':
        form = MyForm(request.POST)
        if form.is_valid():
            message = addToPortfolio(form.cleaned_data)

    data = {'form': form, 'message': message}
    return render(request, 'dashboard_app/dashboard.html', context=data)

def asset(request):
    selectedCoin = 'BTC'
    user = 1
    message = ""
    form = MyForm2(initial={'user': user, 'assetDropdown': selectedCoin})
    if request.method=='POST':
        form = MyForm2(request.POST)
        if form.is_valid():
            message = addToPortfolio(form.cleaned_data)
    data = {'coinInfo': getCoinInformation(selectedCoin), 
            'values':getCryptoValuesFromDatabase(selectedCoin, date(year=2023, month=4, day=19), date(year=2023, month=5, day=11)),
            'form': form,
            'message': message}
    return render(request, 'dashboard_app/asset.html', context=data)


def addToPortfolio(cleanedData):
    if cleanedData.get('purchaseDate') > date.today(): return "You picked a date in the future!"
    date1 = cleanedData.get('purchaseDate')
    if doesCoinExistInDatabase(cleanedData.get('assetDropdown')):
        asset = getAssetFromDatabase(cleanedData.get('assetDropdown'))
        user = getUser(cleanedData.get('user'))
        Portfolio.objects.create(
                user=user, 
                asset=asset, 
                purchaseDate=datetime(date1.year,date1.month,date1.day),
                amount = cleanedData.get('amount')
                )
        return "Success: Asset saved"
    else:
        return "Error: Asset could not be saved"
