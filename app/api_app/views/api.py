from django.shortcuts import render
from django.http import HttpResponse
from api_app.forms import AddAssetData, AddCoin
from api_app.cryptoservice import saveDataFromApiToDatabase, getCoinInformation, addCoinToDatabase
from api_app.databaseservice import getAllCoinsFromDatabase


def api(request):
    addAssetDataMessages = ""
    addAssetDataForm = AddAssetData()
    addCoinForm = AddCoin()
    if request.method=='POST':
        addAssetDataForm = AddAssetData(request.POST)
        if addAssetDataForm.is_valid():
            data = addAssetDataForm.cleaned_data
            dateFrom = data.get('dateFrom')
            dateTo = data.get('dateTo')
            addAssetDataMessages = saveDataFromApiToDatabase(data["asset"], data["currency"], dateFrom, dateTo)
    coins = []
    for coin in getAllCoinsFromDatabase():
        coins.append(coin)
    data = {'addAssetDataForm': addAssetDataForm, 'addCoinForm': addCoinForm,'addAssetDataMessages': addAssetDataMessages, 'coins': coins}
    return render(request, 'api_app/api.html', context=data)

