from django.shortcuts import render
from dashboard_app.models import Portfolio
from datetime import datetime
from api_app.views import getAssetFromDatabase, doesCoinExistInDatabase
from user_app.views import getUser
from dashboard_app.forms import MyForm

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


#TODO aktuellen/historischen Wert der Kryptowährung aus der Datenbank holen und in purchaseValue setzen
#TODO Daten vom purchaseDate bis heute speichern
def addToPortfolio(cleanedData):
    if doesCoinExistInDatabase(cleanedData.get('asset')):
        asset = getAssetFromDatabase(cleanedData.get('asset'))
        user = getUser(cleanedData.get('user'))
        Portfolio.objects.get_or_create(
            user=user, 
            asset=asset, 
            purchaseDate=cleanedData.get('purchaseDate'), 
            purchaseValue=cleanedData.get('purchaseValue')
            )
        return "Success: Asset saved"
    else:
        return "Error: Asset could not be saved"
