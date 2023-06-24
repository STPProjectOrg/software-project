from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from dashboard_app.models import Watchlist, Transaction
from api_app.models import Asset, AssetHistory


def watchlist_add(request, asset_symbol):
    # Try deleting database entry
    asset = Asset.objects.get(name=asset_symbol)
    try:
        Watchlist.objects.get(user=request.user, asset=asset).delete()

    # Else create new entry
    except ObjectDoesNotExist:
        Watchlist.objects.create(user=request.user,
                                   asset=asset, added_at = datetime.now())
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_watchlist(user):
    assets = []
    for watchlist_asset in Watchlist.objects.filter(user=user):
        asset = Asset.objects.get(id=watchlist_asset.asset_id)
        date="2023-05-20"
        d=datetime.strptime(date, "%Y-%m-%d").date()
        price = AssetHistory.objects.get(name_id=asset.id, date=date)
        try:
            pricediff = AssetHistory.objects.get(name_id=asset.id, date=d-timedelta(days=watchlist_asset.price_change))
        except:
            pricediff = AssetHistory.objects.get(name_id=asset.id, date=d-timedelta(days=0))
        pricediffpercent = round((price.value / pricediff.value) - 1,4)
        data = {
            "imageUrl": asset.imageUrl,
            "name": asset.name, 
            "coinName": asset.coinName, 
            "price": price, 
            "pricediff": pricediff, 
            "pricediffpercent":pricediffpercent,
            "added_at": watchlist_asset.added_at,
            "isInPortfolio": Transaction.objects.filter(user=user, asset=asset).exists(),
            "price_change": watchlist_asset.price_change
            }
        assets.insert(0, data)
    return assets


def watchlist_update_asset_price_change(request, asset_symbol, price_change):
    asset = Asset.objects.get(name= asset_symbol)
    Watchlist.objects.filter(user=request.user, asset=asset).update(price_change=price_change)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))