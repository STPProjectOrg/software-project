from django.shortcuts import render
from django.http import HttpResponse
from api_app.forms import AddAssetData
from api_app.cryptoservice import saveDataFromApiToDatabase


# Create your views here.
def api(request):
    message = ""
    form = AddAssetData()
    if request.method=='POST':
        form = AddAssetData(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            dateFrom = data.get('dateFrom')
            dateTo = data.get('dateTo')
            message = saveDataFromApiToDatabase(data["asset"], data["currency"], dateFrom, dateTo)

    data = {'form': form, 'message': message}
    return render(request, 'api_app/api.html', context=data)
