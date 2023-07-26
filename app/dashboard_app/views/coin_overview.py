from dashboard_app.models import Watchlist, WatchlistAsset
from api_app.databaseservice import get_all_assets_from_database

def get_coin_overview(request):
    '''
    Get the currently supported coins and convert them 
    into a custom dictionary to display them easier.
    Checks if the displayed coin exsists in the logged in users 'Watchlist'
    '''

    assets = []
    watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
    for coinasset in get_all_assets_from_database():
        data = {
            "imageUrl": coinasset.imageUrl,
            "name": coinasset.name, 
            "coinName": coinasset.coinName, 
            "isInWatchlist": WatchlistAsset.objects.filter(watchlist=watchlist, asset=coinasset).exists(),
            }
        assets.append(data)
    return assets