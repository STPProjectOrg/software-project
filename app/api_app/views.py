from django.shortcuts import render
from django.http import HttpResponse
from .models import Asset, AssetHistory
from datetime import datetime, timedelta
from .cryptoservice import getCurrentCryptoPrice, getHistoricalCryptoData, getAllCryptoData
from api_app.forms import MyForm
import time


# Create your views here.
def api(request):
    cryptoCurrencyString = ['BTC']
    currencyString = ['EUR']
    
    #addCoinToDatabase('BTC','Bitcoin','EUR')
    #addCoinToDatabase('ETH','Ethereum','EUR')
    #addCoinToDatabase('USDT','Tether','EUR')
    #addCoinToDatabase('XRP','XRP','EUR')
    #saveDataFromApiToDatabase('BTC', 'EUR', dateFrom, dateTo)
    
    #values = getCryptoValuesFromDatabase('BTC', 2022, 2022)
    message = ""
    form = MyForm()
    if request.method=='POST':
        form = MyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            dateFrom = data.get('dateFrom')
            dateTo = data.get('dateTo')
            values = getCryptoValuesFromDatabase('BTC', dateFrom, dateTo)
            message = "s"

    #print(getCoinInformation("BTC"))
    data = {'value':values, 'crypto': cryptoCurrencyString, 'currency': currencyString, 'historicalPrice': 0, 'historicalDate': 0, 'form': form, 'message': message}
    return render(request, 'api_app/api.html', context=data)

#Die Funktion gibt den Wert der Kryptowährung zum gegebenen Datum zurück
#Beispielaufruf: getCryptoValueFromDatabase('USDT', datetime(2023,4,28))
def getCryptoValueFromDatabase(cryptoCurrencyString, date):
    asset = Asset.objects.get(name=cryptoCurrencyString).pk
    return AssetHistory.objects.get_or_create(date=date, name=asset)[0]

#Die Funktion gibt die Werte der Kryptowährung aus der Datenbank zurück
#Beispielaufruf: getCryptoValuesFromDatabase('BTC', dateFrom, dateTo)
def getCryptoValuesFromDatabase(cryptoCurrencyString, dateFrom, dateTo):
    asset = Asset.objects.get(name=cryptoCurrencyString)
    dateDiff = dateTo - dateFrom 
    data = []
    for month in range(dateFrom.month, dateTo.month+1):
        print(month)
    for days in range(dateDiff.days + 1):
        date = dateFrom + timedelta(days=days)
        if AssetHistory.objects.filter(date=date, name=asset).exists():
            data.append(AssetHistory.objects.get_or_create(date=date, name=asset)[0].value)
        else:
            print(f"Value for {date} does not exist")
    return data

#Fügt eine neue Kryptowährung der Datenbank hinzu 
#und dessen dazugehörige Historie für den heutigen Tag
#Beispielaufruf: addCoinToDatabase('BTC','Bitcoin','EUR')
def addCoinToDatabase(cryptoCurrencyString, coinName, currencyString):
    if not doesCoinExistInAPI(cryptoCurrencyString): 
        return print(f"{cryptoCurrencyString} not supported from the API")
    if getAssetFromDatabase(cryptoCurrencyString).name == cryptoCurrencyString: 
        return print(f"{cryptoCurrencyString} already exists in database")

    asset = Asset.objects.get_or_create(name=cryptoCurrencyString, coinName=coinName)[0]
    currentDate = datetime.now()
    date = datetime(currentDate.year,currentDate.month,currentDate.day)
    currentCryptoPrice = getCurrentCryptoPrice(cryptoCurrencyString)[cryptoCurrencyString][currencyString]
    AssetHistory.objects.get_or_create(date=date, value=currentCryptoPrice, name=asset)[0]

        
#Fügt der angegebenen Kryptowährungshistorie historische Daten hinzu
#Der Beispielaufruf fügt vom 01.01.2017 bi zum 31.12.2017 der Datenbank tägliche Kursdaten hinzu
#Aktuell nur den Tageswert.
#Beispielaufruf: saveYearlyDataToDatabase('BTC', 'EUR', dateFrom, dateTo)
def saveDataFromApiToDatabase(cryptoCurrency, currency, dateFrom, dateTo):
    dateDiff = dateTo - dateFrom 
    asset = Asset.objects.get(name=cryptoCurrency)
    for days in range(dateDiff.days + 1):
        historicalDate = dateFrom + timedelta(days=days)
        if AssetHistory.objects.filter(date=historicalDate, name=asset).exists():
            print("value exists already")
        else:
            historicalPrice = getHistoricalCryptoData(cryptoCurrency, currency, historicalDate)
            AssetHistory.objects.get_or_create(date=historicalDate, value=historicalPrice[cryptoCurrency][currency], name=asset)[0]
            time.sleep(0.33)


#Sucht ein Asset in der Datenbank nach dem Namen oder Kürzel der Kryptowährung
#assetString kann das Kürzel oder der Name der Kryptowährung sein
def getAssetFromDatabase(assetString):
    if Asset.objects.filter(name=assetString).exists():
        asset = Asset.objects.get(name=assetString)
    elif Asset.objects.filter(coinName=assetString).exists():
        asset = Asset.objects.get(coinName=assetString)
    else:
        asset = Asset(name="N/A", coinName="N/A")
    return asset

#Sucht ein Asset in der API und überprüft, ob das Asset verfügbar ist
#assetString muss ein Kürzel sein z.B. 'BTC'
def doesCoinExistInAPI(assetString):
    for asset in getAllCryptoData(formatted=True):
        if assetString == asset:
            return True
    return False

#Sucht ein Asset in der Datenbank und überprüft, ob das Asset verfügbar ist
#assetString muss ein Kürzel sein z.B. 'BTC' oder der Name z.B. 'Bitcoin'
def doesCoinExistInDatabase(assetString):
    if getAssetFromDatabase(assetString).name != "N/A":
        return True
    else:
        return False


#Fragt Informationen von der API zur angegebenen Kryptowährung(Kürzel) ab
#assetString muss ein Kürzel sein z.B. 'BTC'
def getCoinInformation(assetString):
    if doesCoinExistInAPI(assetString):
        return getAllCryptoData(formatted=False)[assetString]
    return f"Cryptocurrency {assetString} not supported"


