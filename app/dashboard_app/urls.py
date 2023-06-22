from django.urls import re_path, path
from dashboard_app import views
from dashboard_app.views import main, transaction, watchlist

app_name = 'dashboard_app'

urlpatterns = [
    re_path('dashboard', main.dashboard, name="dashboard"),
    path('asset/<str:coin>', main.asset, name="asset"),
    path('watchlist', main.watchlist, name="watchlist"),
    path('watchlist/<str:asset_symbol>', watchlist.watchlist_add, name="watchlist_add"),

    # Transaction
    path("transaction/buy/<str:coin>", transaction.buy, name="transaction_buy")
]
