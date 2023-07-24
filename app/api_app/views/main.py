from django.shortcuts import render
from api_app.forms import AddAssetDataForm, AddCoinForm
from api_app.databaseservice import get_all_assets_from_database

def api_admin_panel(request):
    """ Render the api admin panel page. """

    data =  {
            'add_asset_data_form': AddAssetDataForm(),
            'add_coin_form': AddCoinForm(), 
            'coins': get_all_assets_from_database()
            }
    
    return render(request, 'api_app/api_admin_panel.html', context=data)

