from django.urls import path
from dashboard_app.views import main, transaction, watchlist


app_name = 'dashboard_app'

urlpatterns = [
    # Overview
    path('<int:timespan>', main.dashboard, name="dashboard"),

    # Asset
    path('asset/<str:name>/<int:timespan>', main.asset, name="asset"),

    # Coin Overview
    path('coin_overview/', main.coin_overview, name="coin_overview"),

    # Watchlist
    path('watchlist/list/<str:username>/<str:sort_by>',
         main.watchlist, name="watchlist"),
    path('watchlist/add/<str:asset_symbol>',
         watchlist.watchlist_add, name="watchlist_add"),
    path('watchlist/price_change/<str:asset_symbol>/<int:price_change>',
         watchlist.watchlist_update_asset_price_change, name="watchlist_update_asset_price_change"),
    path('watchlist/like/<int:watchlist_id>',
         watchlist.like_watchlist, name='like_watchlist'),

    # Transaction
    path("transaction/list", main.transactions, name="transactions"),
    path("transaction/add/<str:coin>", transaction.add, name="transaction_add"),
    path("transaction/delete/<int:transaction_id>",
         transaction.delete, name="transaction_delete"),
    path("transaction/update/<int:transaction_id>",
         transaction.update, name="transaction_update"),
]
