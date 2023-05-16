from django.shortcuts import render
from django.template import RequestContext
from dashboard_app.models import Portfolio
from api_app.models import AssetHistory
from core.models import History
from datetime import datetime, date, timedelta
from api_app.views import getAssetFromDatabase, doesCoinExistInDatabase, getCryptoValueFromDatabase, saveDataFromApiToDatabase
from user_app.views import getUser
from dashboard_app.forms import MyForm
from dateutil.relativedelta import relativedelta

# Create your views here.
def dashboard(request):
    message = ""
    form = MyForm()
    if request.method=='POST':
        form = MyForm(request.POST)
        if form.is_valid():
            message = addToPortfolio(form.cleaned_data)

    pieData = getDataForPie(request.user)
    chartData = getDataForLine(request.user)
    data = {**{'form': form, 'message': message},**pieData, **chartData}
    return render (request, 'dashboard_app/dashboard.html', data)

def getAllUserAssets(user):
    allAssets = Portfolio.objects.filter(user = user.id)
    return allAssets


def getAllUniqueAssets(allAssets):
    assetList = list()
    for thisAsset in allAssets.all():
        if thisAsset.asset not in assetList:
            assetList.append(thisAsset.asset)
    return assetList

def getDataForPie(user):
    allAssets = getAllUserAssets(user)
    assetList = getAllUniqueAssets(allAssets)
    pieList = list()
    assetNameList = list()
    for thisAsset in assetList:
        assetNameList.append(thisAsset.name)
        temp = allAssets.filter(asset = thisAsset)
        tempAmount = 0
        for tempAsset in temp:
            tempAmount += tempAsset.amount
        pieList.append([thisAsset, tempAmount])
    valueList = list()
    for element in pieList:
        currentVal = float(getAssetValue(element[0], date.today()))
        valueList.append(currentVal*element[1])
    data = {'assetList' : assetNameList, 'values': valueList}
    return data

def getDataForLine(user):
    sorted = Portfolio.objects.filter(user = user.id).order_by('purchaseDate')
    today = date.today()
    beginning = sorted.first().purchaseDate
    uniqueAssets = list()
    months = getMonths(beginning, today)
    for thisAsset in sorted:
        if thisAsset.asset not in uniqueAssets:
            for month in months:
                createHistory(thisAsset.asset, month, month - timedelta(1))
            uniqueAssets.append(thisAsset)
    dateValues = list()
    for IterDate in months:
        dateVal = 0
        for thisAsset in sorted:
            if thisAsset.purchaseDate <= IterDate:
                dateVal += thisAsset.amount*float(getAssetValue(thisAsset.asset, IterDate))
        dateValues.append(dateVal)
    data = {'months' : months, 'dateValues' : dateValues}
    return data

def getMonths(beginning, today):
    monthsList = list()
    iterDate = beginning
    while iterDate.month <= today.month :
        monthsList.append(iterDate)
        iterDate = iterDate + relativedelta(months = 1)
    return monthsList


def getAssetValue(thisAsset, date):
    todaysHistory = AssetHistory.objects.get(name = thisAsset, date = date)
    currentVal =todaysHistory.value
    return currentVal

def createHistory(thisAsset, dateTo, dateFrom):
    saveDataFromApiToDatabase(thisAsset.name, 'EUR', dateFrom, dateTo)
    

def addToPortfolio(cleanedData):
    if cleanedData.get('purchaseDate') > date.today(): return "You picked a date in the future!"
    date1 = cleanedData.get('purchaseDate')
    #print(cleanedData.get('assetDropdown'))
    if doesCoinExistInDatabase(cleanedData.get('assetDropdown')):
        asset = getAssetFromDatabase(cleanedData.get('assetDropdown'))
        user = getUser(cleanedData.get('user'))
        Portfolio.objects.create(
                user=user, 
                asset=asset, 
                purchaseDate=datetime(date1.year,date1.month,date1.day),
                amount = cleanedData.get('amount')
                )
        return "Success: Asset saved"
    else:
        return "Error: Asset could not be saved"
