from django.shortcuts import render
from django.http import HttpResponse
from .cryptoservice import getCurrentCryptoPrice, getHistoricalCryptoData, getAll
import datetime

# Create your views here.
def api(request):
    cryptoCurrencyString = ['BTC']
    currencyString = ['EUR']
    historicalDate = datetime.datetime(2017,6,6)
    currentCryptoPrice = getCurrentCryptoPrice(cryptoCurrencyString)
    
    historicalPrice = getHistoricalCryptoData(cryptoCurrencyString[0], currencyString[0], historicalDate)
    data = {'value':currentCryptoPrice[cryptoCurrencyString[0]][currencyString[0]], 'crypto': cryptoCurrencyString, 'currency': currencyString, 'historicalPrice': historicalPrice[cryptoCurrencyString[0]][currencyString[0]], 'historicalDate': historicalDate}
    return render(request, 'api_app/api.html', context=data)