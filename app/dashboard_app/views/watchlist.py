from datetime import datetime, timedelta, date 
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from dashboard_app.models import Watchlist, Transaction, WatchlistLike, WatchlistAsset
from api_app.models import Asset, AssetHistory

def watchlist_add(request, asset_symbol):
    # Try deleting database entry
    asset = Asset.objects.get(name=asset_symbol)
    watchlist = Watchlist.objects.get(user = request.user)
    try:
        WatchlistAsset.objects.get(watchlist=watchlist, asset=asset).delete()

    # Else create new entry
    except ObjectDoesNotExist:
        WatchlistAsset.objects.create(watchlist=watchlist,
                                   asset=asset, added_at = datetime.now())
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_watchlist(user, watchlist, sort_by):
    assets = []
    for watchlist_asset in WatchlistAsset.objects.filter(watchlist=watchlist):
        asset = Asset.objects.get(id=watchlist_asset.asset_id)
        ##Muss zum testen auf "2023-05-20" geändert werden
        today = "2023-05-20"#str(date.today())
        d=datetime.strptime(today, "%Y-%m-%d").date()
        price = AssetHistory.objects.get(name_id=asset.id, date=today)
        try:
            pricediff = AssetHistory.objects.get(name_id=asset.id, date=d-timedelta(days=watchlist_asset.price_change))
        except:
            pricediff = AssetHistory.objects.get(name_id=asset.id, date=d-timedelta(days=0))
        pricediffpercent = round((price.value / pricediff.value) - 1,4)
        data = {
            "imageUrl": asset.imageUrl,
            "name": asset.name, 
            "coinName": asset.coinName, 
            "price": price.value, 
            "pricediff": pricediff.value, 
            "pricediffpercent":pricediffpercent,
            "added_at": watchlist_asset.added_at,
            "isInWatchlist": WatchlistAsset.objects.filter(watchlist=watchlist,asset=asset).exists(),
            "isInPortfolio": Transaction.objects.filter(user=user, asset=asset).exists(),
            "price_change": watchlist_asset.price_change,
            }
        assets.insert(0, data)

    return handle_sort_by(assets, sort_by)

def handle_sort_by(assets, sort_by):
    match sort_by:
        case "nameAsc": return sorted(assets, key=lambda item: item["name"])
        case "nameDesc": return sorted(assets, key=lambda item: item["name"])[::-1]
        case "coinNameAsc": return sorted(assets, key=lambda item: item["coinName"])
        case "coinNameDesc": return sorted(assets, key=lambda item: item["coinName"])[::-1]
        case "priceAsc": return sorted(assets, key=lambda item: item["price"])
        case "priceDesc": return sorted(assets, key=lambda item: item["price"])[::-1]
        case "pricediffAsc": return sorted(assets, key=lambda item: item["pricediff"])
        case "pricediffDesc": return sorted(assets, key=lambda item: item["pricediff"])[::-1]
        case "pricediffpercentAsc": return sorted(assets, key=lambda item: item["pricediffpercent"])
        case "pricediffpercentDesc": return sorted(assets, key=lambda item: item["pricediffpercent"])[::-1]
        case "added_atAsc": return sorted(assets, key=lambda item: item["added_at"])
        case "added_atDesc": return sorted(assets, key=lambda item: item["added_at"])[::-1]
        case "isInWatchlistAsc": return sorted(assets, key=lambda item: item["isInWatchlist"])
        case "isInWatchlistDesc": return sorted(assets, key=lambda item: item["isInWatchlist"])[::-1]
        case "isInPortfolioAsc": return sorted(assets, key=lambda item: item["isInPortfolio"])
        case "isInPortfolioDesc": return sorted(assets, key=lambda item: item["isInPortfolio"])[::-1]
        case _: return assets



def watchlist_update_asset_price_change(request, asset_symbol, price_change):
    asset = Asset.objects.get(name= asset_symbol)
    watchlist = Watchlist.objects.get(user=request.user)
    WatchlistAsset.objects.filter(watchlist=watchlist, asset=asset).update(price_change=price_change)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def like_watchlist(request, watchlist_id):
    """
    Toggles a 'WatchlistLikes' entrie by a given watchlist_id and the requesting user.

    Keyword arguments:
        watchlist_id: The id of the 'Watchlist' to be liked.
    """

    # Try deleting database entry
    try:
        WatchlistLike.objects.filter(
            user=request.user.id, watchlist=watchlist_id).get().delete()

    # Else create new entry
    except ObjectDoesNotExist:
        WatchlistLike.objects.create(user=request.user,
                                   watchlist=Watchlist.objects.get(id=watchlist_id))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

