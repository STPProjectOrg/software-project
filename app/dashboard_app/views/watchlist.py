from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from dashboard_app.models import Watchlist
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
        price = AssetHistory.objects.get(name_id=asset.id, date="2023-05-20")
        data = {"name": asset.name, "coinName": asset.coinName, "price": price,"added_at": watchlist_asset.added_at}
        assets.insert(0, data)
    return assets