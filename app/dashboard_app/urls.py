from django.urls import re_path, path
from dashboard_app import views
from dashboard_app.views import main, transaction, watchlist

app_name = 'dashboard_app'

urlpatterns = [
    re_path('dashboard', main.view_dashboard, name="dashboard"),
    path('asset/<str:name>', main.view_asset, name="asset"),

    # Watchlist
    path('watchlist', main.watchlist, name="watchlist"),
    path('watchlist/<str:asset_symbol>',
         watchlist.watchlist_add, name="watchlist_add"),
    path('watchlist/price_change/<str:asset_symbol>/<int:price_change>',
         watchlist.watchlist_update_asset_price_change, name="watchlist_update_asset_price_change"),

    # Transaction
    path("transaction/buy/<str:coin>", transaction.buy, name="transaction_buy")
]
