import cryptocompare
import time
import datetime
from api_app.models import Asset, AssetHistory

cryptocompare.cryptocompare._set_api_key_parameter('24b0b1c73aa9e5a995c51d76ebad08bd0e352d235ed9bacf56184d7a2cfb8296')

def get_current_crypto_price(crypto_asset: str) -> float:
    """
    Get the current value from an asset provided by the api.

    Keyword arguments:
        crypto_asset:   The asset to get the value from, given as symbol.
    """
    currentCryptoPrice = cryptocompare.get_price(crypto_asset)
    return currentCryptoPrice

def get_historical_crypto_data(crypto_asset: str, currency: str, historical_date: str) -> float:
    """
    Get the historical value provided by the api for the provided asset, currency and date.

    Keyword arguments:
        crypto_asset:   The asset to get the value from, given as symbol.
        currency:       The currency.
        historical_date:The historical date.
    """

    historicalCryptoData = cryptocompare.get_historical_price(crypto_asset, currency, historical_date)
    return historicalCryptoData

def get_all_crypto_data(formatted: bool) -> list:
    """
    Get all assets and their information provided by the api.

    Keyword arguments:
        formatted:      Specifies if the list is formatted or not. 
    """

    data = cryptocompare.get_coin_list(format=formatted)
    return data


def does_asset_exist_in_api(crypto_asset: str):
    """
    Check if the given asset is supported by the api.

    Keyword arguments:
        crypto_asset:   The asset to get checked, given as symbol. 
    """

    for crypto_asset in get_all_crypto_data(formatted=True):
        if crypto_asset == crypto_asset:
            return True
    return False

def get_asset_information(crypto_asset: str):
    """
    Get all the provided information about the given asset from the api.

    Keyword arguments:
        crypto_asset:   The asset to get the information from, given as symbol. 
    """

    if does_asset_exist_in_api(crypto_asset):
        return get_all_crypto_data(formatted=False)[crypto_asset]
    return f"Cryptocurrency {crypto_asset} not supported"


def save_data_from_api_to_database(crypto_asset: str, currency: str, date_from: str, date_to: str) -> list [str]:
    """
    Create 'AssetHistory'-Entries for a given asset and a specific timespan.

    Keyword arguments:
        crypto_asset:   The asset to be saved, given as symbol. 
        currency:       The currency in which the value is saved.
        date_from:      The starting date.
        date_to:        The ending date.
    """

    message = []
    date_difference = date_to - date_from 
    asset = Asset.objects.get(name=crypto_asset)
    for days in range(date_difference.days + 1):
        historical_date = date_from + datetime.timedelta(days=days)
        if AssetHistory.objects.filter(date=historical_date, name=asset).exists():
            message.append(f"{historical_date} value exists already")
        else:
            historical_price = get_historical_crypto_data(crypto_asset, currency, historical_date)
            AssetHistory.objects.get_or_create(date=historical_date, value=historical_price[crypto_asset][currency], name=asset)[0]
            time.sleep(0.33)
            message.append(f'{historical_date} wurde hinzugefügt.') 
    return message


def add_asset_to_database(crypto_asset: str, currency: str):
    """
    Create a new 'Asset'-Entry and saves it to the database.
    Create a new 'AssetHistory'-Entry with todays 'Asset' value.

    Keyword arguments:
        crypto_asset:   The asset to be saved, given as symbol. 
        currency:       The currency in which the value is saved.
    """

    try:
        coin = get_asset_information(crypto_asset)
        coin_name = coin['CoinName']
        image = "https://www.cryptocompare.com"+coin['ImageUrl']
        asset = Asset.objects.get_or_create(name=crypto_asset, coinName=coin_name, imageUrl=image)[0]
        current_date = datetime.date.today()
        current_crypto_price = get_current_crypto_price(crypto_asset)[crypto_asset][currency]
        AssetHistory.objects.get_or_create(date=current_date, value=current_crypto_price, name=asset)[0]
        return f"{crypto_asset} wurde erfolgreich der Datenbank hinzugefügt!"
    except:
        return f"{crypto_asset} wird von dir API nicht unterstützt!"
    

