from .models import Asset, AssetHistory
from datetime import timedelta

def get_asset_choices() -> list[(str,str)]:
    asset_choices = []
    for asset in getAllCoinsFromDatabase():
        asset_choices.append((asset.name,asset.coinName))
    return asset_choices

def getAllCoinsFromDatabase() -> list[Asset]:
    return Asset.objects.all()

#Sucht ein Asset in der Datenbank und überprüft, ob das Asset verfügbar ist
#assetString muss ein Kürzel sein z.B. 'BTC' oder der Name z.B. 'Bitcoin'
def doesCoinExistInDatabase(asset: str) -> bool:
    if getAssetFromDatabase(asset).name != "N/A":
        return True
    else:
        return False
    
#Sucht ein Asset in der Datenbank nach dem Namen oder Kürzel der Kryptowährung
#assetString kann das Kürzel oder der Name der Kryptowährung sein
def getAssetFromDatabase(assetString: str) -> Asset:
    if Asset.objects.filter(name=assetString).exists():
        asset = Asset.objects.get(name=assetString)
    elif Asset.objects.filter(coinName=assetString).exists():
        asset = Asset.objects.get(coinName=assetString)
    else:
        asset = Asset(name="N/A", coinName="N/A")
    return asset

#Die Funktion gibt die Werte der Kryptowährung aus der Datenbank zurück
#Beispielaufruf: getCryptoValuesFromDatabase('BTC', dateFrom, dateTo)
def getCryptoValuesFromDatabase(cryptoCurrency: str, dateFrom: str , dateTo: str) -> list[float]:
    asset = Asset.objects.get(name=cryptoCurrency)
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

#Die Funktion gibt den Wert der Kryptowährung zum gegebenen Datum zurück
#Beispielaufruf: getCryptoValueFromDatabase('USDT', datetime(2023,4,28))
def getCryptoValueFromDatabase(cryptoCurrency: str, date: str) -> float:
    asset = Asset.objects.get(name=cryptoCurrency).pk
    return AssetHistory.objects.get_or_create(date=date, name=asset)[0]
