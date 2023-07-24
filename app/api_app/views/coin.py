from django.http import HttpResponseRedirect
from api_app.forms import AddCoinForm
from api_app.cryptoservice import add_asset_to_database
from api_app.cryptoservice import save_data_from_api_to_database
from api_app.forms import AddAssetDataForm

def add_coin(request):
    """ 
    Create a new 'Coin' in database. Gets Information from API 

    Keyword arguments in the form cleaned_data:
        asset: The asset to be saved given as symbol. 
        currency: The currency in which the value is saved.
    """
    
    add_coin_form = AddCoinForm(request.POST)
    if add_coin_form.is_valid():
        data = add_coin_form.cleaned_data
        add_asset_to_database(data['asset'], data['currency'])
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_asset_data(request):
    """ 
    Gets daily coin values for a specific time period. Gets Information from API 

    Keyword arguments in the form cleaned_data:
        asset: The asset to be saved given as symbol. 
        currency: The currency in which the value is saved.
        dateFrom: The starting date.
        dateTo: The ending date.
    """

    add_asset_data_form = AddAssetDataForm(request.POST)
    if add_asset_data_form.is_valid():
        data = add_asset_data_form.cleaned_data
        save_data_from_api_to_database(
                                  data["asset"],
                                  data["currency"], 
                                  data["dateFrom"], 
                                  data["dateTo"]
                                  )
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))