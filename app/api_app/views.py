from django.shortcuts import render
from django.http import HttpResponse
from .cryptoservice import getCurrentCryptoPrice, getHistoricalCryptoData, getAll
from .models import Asset, AssetHistory
import datetime

# Create your views here.
def api(request):
    cryptoCurrencyString = ['BTC']
    currencyString = ['EUR']
    historicalDate = datetime.datetime(2017,6,5)
    #currentCryptoPrice = getCurrentCryptoPrice(cryptoCurrencyString)
    #getYearlyData(cryptoCurrencyString[0], currencyString[0], 2017,2017)
    #historicalPrice = getHistoricalCryptoData(cryptoCurrencyString[0], currencyString[0], historicalDate)
    #addCoin()
    assetBTC = Asset.objects.get(name="BTC").pk
    valueOn = AssetHistory.objects.get(name=assetBTC, date=historicalDate)
    data = {'value':0, 'crypto': cryptoCurrencyString, 'currency': currencyString, 'historicalPrice': valueOn, 'historicalDate': historicalDate}
    return render(request, 'api_app/api.html', context=data)

def addCoin():
    asset = Asset.objects.get_or_create(name="BTC", coinName="Bitcoin")[0]
    for i in range(1,6):
        cryptoCurrencyString = ['BTC']
        currencyString = ['EUR']
        historicalDate = datetime.datetime(2017,6,i)
        historicalPrice = getHistoricalCryptoData(cryptoCurrencyString[0], currencyString[0], historicalDate)
        AssetHistory.objects.get_or_create(date=historicalDate, value=historicalPrice[cryptoCurrencyString[0]][currencyString[0]], name=asset)[0]

def getMonthlyDays(year, month):
    days = 28
    thirtyOneDaysMonth = [1,3,5,7,8,10,12]
    thirtyDaysMonth = [4,6,9,11]
    leapYear = [2000, 2004, 2008, 2012, 2016, 2020, 2024]
    if month in thirtyOneDaysMonth:
        days = 31
    elif month in thirtyDaysMonth:
        days = 30
    
    if year in leapYear and  month == 2:
        days = 29

    return days

#Aufruf: getYearlyData(cryptoCurrencyString[0], currencyString[0], 2017,2017)
def getYearlyData(cryptoCurrency, currency, startYear, endYear):
    for year in range(startYear, endYear+1):
        for month in range(1,13):
            for day in range(1, getMonthlyDays(year,month)+1):
                print(f"{year} {month} {day}")
                #print(getHistoricalCryptoData(cryptoCurrency, currency, datetime.datetime(year,month,day)))

