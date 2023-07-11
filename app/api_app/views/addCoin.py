from django.http import HttpResponseRedirect
from api_app.forms import AddCoin
from api_app.cryptoservice import addCoinToDatabase

def addCoin(request):
    """ Create a new 'Coin' in database. Gets Information from API """
    addCoinForm = AddCoin(request.POST)
    if addCoinForm.is_valid():
        data = addCoinForm.cleaned_data
        addCoinMessage = addCoinToDatabase(data['asset'], data['currency'])
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))