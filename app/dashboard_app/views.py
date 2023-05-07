from django.shortcuts import render
from dashboard_app.models import Portfolio
from datetime import datetime
from api_app.views import getAssetFromDatabase, doesCoinExistInDatabase
from user_app.views import getUser
from dashboard_app.forms import MyForm
from dateutil.relativedelta import relativedelta

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
def addToPortfolio(cleanedData):
    dated = relativedelta(cleanedData.get('purchaseDate'), datetime.now())
    if doesCoinExistInDatabase(cleanedData.get('asset')):
        asset = getAssetFromDatabase(cleanedData.get('asset'))
        user = getUser(cleanedData.get('user'))
        for year in range(datetime.now().year+dated.years, datetime.now().year+1):
            for month in range(datetime.now().month+dated.months, datetime.now().month+1):
                for day in range(datetime.now().day+dated.days, datetime.now().day+1):
                    Portfolio.objects.get_or_create(
                        user=user, 
                        asset=asset, 
                        purchaseDate=datetime(year,month,day), 
                        purchaseValue=cleanedData.get('purchaseValue')
                        )
        return "Success: Asset saved"
    else:
        return "Error: Asset could not be saved"
