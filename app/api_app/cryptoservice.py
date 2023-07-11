import cryptocompare
import time
from datetime import timedelta
from api_app.databaseservice import getAssetFromDatabase
from api_app.models import Asset, AssetHistory

cryptocompare.cryptocompare._set_api_key_parameter('24b0b1c73aa9e5a995c51d76ebad08bd0e352d235ed9bacf56184d7a2cfb8296')

#Gibt den aktuellen Wert der Kryptowährung/en zurück
#Übergabeparameter ist ein Array von Strings mit den Abkürzungen der
#Kryptowährung. Bitcoin = 'BTC'
def getCurrentCryptoPrice(cryptocurrency: str) -> float:
    currentCryptoPrice = cryptocompare.get_price(cryptocurrency)
    return currentCryptoPrice

#Gibt die historischen Werte einer Kryptowährung zurück
#Übergabeparameter ist das Kürzel der Kryptowährung, Kürzel Währung und Datum
#date = datetime.datetime(2017,6,6)
def getHistoricalCryptoData(cryptocurrency: str, currency: str, date: str) -> float:
    historicalCryptoData = cryptocompare.get_historical_price(cryptocurrency, currency, date)
    return historicalCryptoData

def getAllCryptoData(formatted: bool) -> list:
    data = cryptocompare.get_coin_list(format=formatted)
    return data

#Sucht ein Asset in der API und überprüft, ob das Asset verfügbar ist
#assetString muss ein Kürzel sein z.B. 'BTC'
def doesCoinExistInAPI(asset: str):
    for asset in getAllCryptoData(formatted=True):
        if asset == asset:
            return True
    return False

#Fragt Informationen von der API zur angegebenen Kryptowährung(Kürzel) ab
#assetString muss ein Kürzel sein z.B. 'BTC'
def getCoinInformation(asset: str):
    if doesCoinExistInAPI(asset):
        return getAllCryptoData(formatted=False)[asset]
    return f"Cryptocurrency {asset} not supported"

#Fügt der angegebenen Kryptowährungshistorie historische Daten hinzu
#Der Beispielaufruf fügt vom 01.01.2017 bi zum 31.12.2017 der Datenbank tägliche Kursdaten hinzu
#Aktuell nur den Tageswert.
#Beispielaufruf: saveYearlyDataToDatabase('BTC', 'EUR', dateFrom, dateTo)
def saveDataFromApiToDatabase(cryptoCurrency: str, currency: str, dateFrom: str, dateTo: str) -> str:
    message = ""
    dateDiff = dateTo - dateFrom 
    asset = Asset.objects.get(name=cryptoCurrency)
    for days in range(dateDiff.days + 1):
        historicalDate = dateFrom + timedelta(days=days)
        if AssetHistory.objects.filter(date=historicalDate, name=asset).exists():
            message += f"{historicalDate} value exists already\n"
        else:
            historicalPrice = getHistoricalCryptoData(cryptoCurrency, currency, historicalDate)
            historicalPrice
            AssetHistory.objects.get_or_create(date=historicalDate, value=historicalPrice[cryptoCurrency][currency], name=asset)[0]
            time.sleep(0.33)
            message += f'{historicalDate} wurde hinzugefügt.\n' 
    return message

#Fügt eine neue Kryptowährung der Datenbank hinzu 
#und dessen dazugehörige Historie für den heutigen Tag
#Beispielaufruf: addCoinToDatabase('BTC','Bitcoin','EUR')
def addCoinToDatabase(cryptoCurrencyString: str, coinName: str, currencyString: str):
    if not doesCoinExistInAPI(cryptoCurrencyString): 
        return print(f"{cryptoCurrencyString} not supported from the API")
    if getAssetFromDatabase(cryptoCurrencyString).name == cryptoCurrencyString: 
        return print(f"{cryptoCurrencyString} already exists in database")

    asset = Asset.objects.get_or_create(name=cryptoCurrencyString, coinName=coinName, imageUrl="https://www.cryptocompare.com"+getCoinInformation(cryptoCurrencyString)['ImageUrl'])[0]
    #currentDate = datetime.now()
    #date = datetime(currentDate.year,currentDate.month,currentDate.day)
    #currentCryptoPrice = getCurrentCryptoPrice(cryptoCurrencyString)[cryptoCurrencyString][currencyString]
    #AssetHistory.objects.get_or_create(date=date, value=currentCryptoPrice, name=asset)[0]
