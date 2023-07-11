from django.urls import path
from api_app.views import addCoin, api
app_name = 'api_app'

urlpatterns = [
    path('api', api.api, name="api"),
    path('api/addCoin', addCoin.addCoin, name="addCoin")
]