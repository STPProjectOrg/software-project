from django.shortcuts import render
from django.http import HttpResponse
from .cryptoservice import getCurrentCryptoPrice, getHistoricalCryptoData, getAll
from .models import Asset, AssetHistory
from datetime import datetime
import time

# Create your views here.
def api(request):
    cryptoCurrencyString = ['BTC']
    currencyString = ['EUR']

    #addCoinToDatabase('BTC','Bitcoin','EUR')
    saveYearlyDataToDatabase('BTC', 'EUR', 2022, 2022)
    
    data = {'value':0, 'crypto': cryptoCurrencyString, 'currency': currencyString, 'historicalPrice': 0, 'historicalDate': 0}
    return render(request, 'api_app/api.html', context=data)


#Die Funktion gibt den Wert der Kryptowährung zum gegebenen Datum zurück
#Beispielaufruf: getCryptoValueFromDatabase('USDT', datetime(2023,4,28))
def getCryptoValueFromDatabase(cryptoCurrencyString, date):
    asset = Asset.objects.get(name=cryptoCurrencyString).pk
    return AssetHistory.objects.get_or_create(date=date, name=asset)[0]

#Fügt eine neue Kryptowährung der Datenbank hinzu 
#und dessen dazugehörige Historie für den heutigen Tag
#Beispielaufruf: addCoinToDatabase('BTC','Bitcoin','EUR')
def addCoinToDatabase(cryptoCurrencyString, coinName, currencyString):
    asset = Asset.objects.get_or_create(name=cryptoCurrencyString, coinName=coinName)[0]
    currentDate = datetime.now()
    date = datetime(currentDate.year,currentDate.month,currentDate.day)
    currentCryptoPrice = getCurrentCryptoPrice(cryptoCurrencyString)[cryptoCurrencyString][currencyString]
    AssetHistory.objects.get_or_create(date=date, value=currentCryptoPrice, name=asset)[0]

#Fügt der angegebenen Kryptowährungshistorie historische Daten hinzu im Jahrestakt
#Der Beispielaufruf fügt vom 01.01.2017 bi zum 31.12.2017 der Datenbank tägliche Kursdaten hinzu
#Aktuell nur den Tageswert.
#Beispielaufruf: saveYearlyDataToDatabase('BTC', 'EUR', 2017, 2017)
def saveYearlyDataToDatabase(cryptoCurrency, currency, startYear, endYear):
    for year in range(startYear, endYear+1):
        for month in range(1,13):
            saveMonthlyDataToDatabase(cryptoCurrency, currency, year, month)

#Fügt der angegebenen Kryptowährungshistorie historische Daten hinzu im Monatstakt
#Der Beispielaufruf fügt vom 01.01.2017 bi zum 31.01.2017 der Datenbank tägliche Kursdaten hinzu
#Aktuell nur den Tageswert.
#Überprüft vor dem Request an die API, ob der Wert schon existiert, um unnötige API-Requests zu vermeiden
#Beispielaufruf: saveMonthlyDataToDatabase('BTC', 'EUR', 2017, 1)
def saveMonthlyDataToDatabase(cryptoCurrency, currency, year, month):
    asset = Asset.objects.get(name=cryptoCurrency)
    for day in range(1, getMonthlyDays(year,month)+1):
        historicalDate = datetime(year,month,day)
        if AssetHistory.objects.filter(date=historicalDate, name=asset).exists():
            print("value exists already")
        else:
            historicalPrice = getHistoricalCryptoData(cryptoCurrency, currency, historicalDate)
            AssetHistory.objects.get_or_create(date=historicalDate, value=historicalPrice[cryptoCurrency][currency], name=asset)[0]
            time.sleep(1)


#Hilfsfunktion für saveYearlyDataToDatabase und saveMonthlyDataToDatabase,
#um die richtige Anzahl von
#Monatstagen herauszufinden
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