from django.shortcuts import render
from dashboard_app.models import Portfolio
from datetime import datetime
from api_app.views import getAssetFromDatabase
from user_app.views import getUser

# Create your views here.
def dashboard(request):
    data = {'value': 0}
    addToPortfolio()
    return render(request, 'dashboard_app/dashboard.html', context=data)


#def addToPortfolio(user, asset, purchaseDate, purchaseValue):
def addToPortfolio():
    currentDate = datetime.now()
    date = datetime(currentDate.year,currentDate.month,currentDate.day)
    asset = getAssetFromDatabase('BTC')
    user = getUser(1)
    Portfolio.objects.get_or_create(user=user, asset=asset, purchaseDate=date, purchaseValue=5)