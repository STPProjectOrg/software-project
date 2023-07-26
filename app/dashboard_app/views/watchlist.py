from datetime import datetime, timedelta, date
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from dashboard_app.models import Watchlist, Transaction, WatchlistAsset
from api_app.models import Asset, AssetHistory

def watchlist_add(request, asset_symbol):
    """
    Add a 'WatchlistAsset' to the logged in users 'Watchlist'.

    Keyword arguments:
        asset_symbol:       The 'Asset' given as symbol.
    """
        
    # Try deleting database entry
    asset = Asset.objects.get(name=asset_symbol)
    watchlist = Watchlist.objects.get(user=request.user)
    try:
        WatchlistAsset.objects.get(watchlist=watchlist, asset=asset).delete()

    # Else create new entry
    except ObjectDoesNotExist:
        WatchlistAsset.objects.create(watchlist=watchlist,
                                      asset=asset, added_at=datetime.now())

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def convert_watchlist(watchlist, sort_by_attribute, direction):
    """
    Convert the 'Watchlist' of the provided user to a custom dictionary.

    Keyword arguments:
        watchlist:          The 'Watchlist' to convert.
        sort_by_attribute:  The attribute to be sorted by.
        direction:          The sorting direction - Ascending 'asc' or Descending 'desc'.
    """
        
    assets = []
    for watchlist_asset in WatchlistAsset.objects.filter(watchlist=watchlist):

        current_price = calculate_price_difference(watchlist_asset.asset.id, 0)
        price_difference = calculate_price_difference(watchlist_asset.asset.id, watchlist_asset.price_change)

        data = {
            "imageUrl": watchlist_asset.asset.imageUrl,
            "name": watchlist_asset.asset.name,
            "coinName": watchlist_asset.asset.coinName,
            "price": current_price.value,
            "pricediff": price_difference.value,
            "pricediffpercent": round(((current_price.value / price_difference.value) - 1) * 100, 4),
            "added_at": watchlist_asset.added_at,
            "isInWatchlist": WatchlistAsset.objects.filter(watchlist=watchlist, asset=watchlist_asset.asset).exists(),
            "isInPortfolio": Transaction.objects.filter(user=watchlist.user, asset=watchlist_asset.asset).exists(),
            "price_change": watchlist_asset.price_change,
        }
        assets.insert(0, data)

    return sort_watchlist_by(assets, sort_by_attribute, direction)

def calculate_price_difference(asset_id, price_change):
    """
    Calculates the price difference of an asset by the provided time and todays date.

    Keyword arguments:
        asset_id:           ID of the asset.
        price_change:       The price_change in days that is saved in the 'WatchlistAsset'.
    """
        
    try:
        return AssetHistory.objects.get(
            name_id=asset_id, 
            date=date.today() - timedelta(days=price_change))
    except:
        return AssetHistory.objects.filter(
            name_id=asset_id).order_by('-date')[0]


def sort_watchlist_by(assets, sort_by_attribute, direction):
    """
    Simply handles the sorting of a 'Watchlist'.

    Keyword arguments:
        sort_by_attribute: The attribute to be sorted by.
        direction:         The sorting direction - Ascending 'asc' or Descending 'desc'.
    """

    if direction == 'asc':
        return sorted(assets, key=lambda item: item[sort_by_attribute])
    elif direction == 'desc':
        return sorted(assets, key=lambda item: item[sort_by_attribute])[::-1]
    else:
        return assets

def watchlist_update_asset_price_change(request, asset_symbol, price_change_time):
    """
    Update the 'price_change' attribute of an 'WatchlistAsset'-Entry.

    Keyword arguments:
        asset_symbol:       The Asset in Watchlist to be updated.
        price_change_time:  The price_change_time to be updated in days given by dropdown-menu in watchlist.
    """

    WatchlistAsset.objects.filter(
        watchlist=Watchlist.objects.get(user=request.user), 
        asset=Asset.objects.get(name=asset_symbol)).update(price_change=price_change_time)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


