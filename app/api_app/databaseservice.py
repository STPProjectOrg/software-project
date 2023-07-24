from .models import Asset, AssetHistory
from datetime import timedelta

def get_asset_choices() -> list[(str,str)]:
    """
    Get all 'Asset'-Entries from the database and converts it into a list of tuples
    with their name and symbol.

    """
        
    asset_choices = []
    for asset in get_all_assets_from_database():
        asset_choices.append((asset.name,asset.coinName))
    return asset_choices

def get_all_assets_from_database() -> list[Asset]:
    """
    Get all 'Asset'-Entries from the database.

    """

    return Asset.objects.all()


def does_asset_exist_in_database(crypto_asset: str) -> bool:
    """
    Check if an 'Asset' exists in the database.

    Keyword arguments:
        crypto_asset:   The asset to check, given as symbol. 
    """

    if get_asset_from_database(crypto_asset).name != "N/A":
        return True
    else:
        return False
    
def get_asset_from_database(crypto_asset: str) -> Asset:
    """
    Get an 'Asset'-Entry for the given asset from the database.

    Keyword arguments:
        crypto_asset:   The asset to get, given as symbol. 

    """

    if Asset.objects.filter(name=crypto_asset).exists():
        asset = Asset.objects.get(name=crypto_asset)
    elif Asset.objects.filter(coinName=crypto_asset).exists():
        asset = Asset.objects.get(coinName=crypto_asset)
    else:
        asset = Asset(name="N/A", coinName="N/A")
    return asset

def get_asset_values_from_database(crypto_asset: str, date_from: str , date_to: str) -> list[float]:
    """
    Get 'AssetHistory'-Entries for a given asset and a specific timespan from the database.

    Keyword arguments:
        crypto_asset:   The asset to get the 'AssetHistory'-Entry for, given as symbol. 
        date_from:      The starting date.
        date_to:        The ending date.
    """
        
    asset = Asset.objects.get(name=crypto_asset)
    date_difference = date_to - date_from 
    data = []
    for days in range(date_difference.days + 1):
        date = date_from + timedelta(days=days)
        if AssetHistory.objects.filter(date=date, name=asset).exists():
            data.append(AssetHistory.objects.get_or_create(date=date, name=asset)[0].value)
        else:
            print(f"Value for {date} does not exist")
    return data

 
def get_asset_value_from_database(crypto_asset: str, date: str) -> float:
    """
    Get the value provided by the database for the provided asset and date.

    Keyword arguments:
        crypto_asset:   The asset to get the value from, given as symbol.
        date:           The historical date.
    """
    asset = Asset.objects.get(name=crypto_asset).pk
    return AssetHistory.objects.get_or_create(date=date, name=asset)[0]
