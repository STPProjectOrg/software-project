from django.urls import path
from api_app.views import coin, main
app_name = 'api_app'

urlpatterns = [
    #Main
    path('api', main.api_admin_panel, name="api_admin_panel"),

    #Coin
    path('api/add/coin', coin.add_coin, name="add_coin"),
    path('api/add/asset_data', coin.add_asset_data, name="add_asset_data"),
]