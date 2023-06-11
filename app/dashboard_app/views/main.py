from django.shortcuts import render
from django.template import RequestContext
from dashboard_app.models import Transaction
from api_app.models import Asset, AssetHistory
from core.models import History
from datetime import datetime, date, timedelta
from datetime import datetime, date
from api_app.views import getAssetFromDatabase, doesCoinExistInDatabase, getCoinInformation, getCryptoValuesFromDatabase, getCryptoValueFromDatabase, saveDataFromApiToDatabase

from user_app.views import getUser
from dashboard_app.forms import MyForm, MyForm2
from dateutil.relativedelta import relativedelta


# Create your views here.
def dashboard(request):
    message = ""
    form = MyForm()
    todaysDate = date.fromisoformat('2023-05-20')
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            message = addToPortfolio(form.cleaned_data)

    if 'complete' in request.POST:
        chartData = getDataForLine(
            request.user, date.min, relativedelta(days=1))
    else:
        if 'month' in request.POST:
            chartData = getDataForLine(
                request.user, todaysDate - relativedelta(months=1), relativedelta(days=1))
        else:
            if 'week' in request.POST:
                chartData = getDataForLine(
                    request.user, todaysDate - timedelta(days=7), relativedelta(days=1))
            else:
                if 'sixmonths' in request.POST:
                    chartData = getDataForLine(
                        request.user, todaysDate - relativedelta(months=6), relativedelta(days=1))
                else:
                    if 'year' in request.POST:
                        chartData = getDataForLine(
                            request.user, todaysDate - relativedelta(years=1), relativedelta(days=1))
                    else:
                        chartData = getDataForLine(
                            request.user, date.min, relativedelta(days=1))

    pieData = getDataForPie(request.user)
    data = {**{'form': form, 'message': message}, **pieData, **chartData}
    return render(request, 'dashboard_app/dashboard.html', data)


def getAllUserAssets(user):
    allAssets = Transaction.objects.filter(user=user.id)
    return allAssets


def getAllUniqueAssets(allAssets):
    assetList = list()
    for thisAsset in allAssets.all():
        if thisAsset.asset not in assetList:
            assetList.append(thisAsset.asset)
    return assetList


def getDataForPie(user):
    allAssets = getAllUserAssets(user)
    if not allAssets:
        return {'assetList': list(), 'values': list()}
    else:
        assetList = getAllUniqueAssets(allAssets)
        assetNameList = list()
        valueList = list()
        for thisAsset in assetList:
            assetNameList.append(thisAsset.name)
            temp = allAssets.filter(asset=thisAsset)
            tempAmount = 0
            for tempAsset in temp:
                tempAmount += tempAsset.amount
            currentVal = float(getAssetValue(
                thisAsset, date.fromisoformat('2023-05-20')))
            valueList.append(currentVal*tempAmount)
        data = {'assetList': assetNameList, 'values': valueList}
        return data


def getDataForLine(user, dateFrom, timeInterval):
    sortedTransactions = Transaction.objects.filter(
        user=user.id).order_by('purchaseDate')
    if not sortedTransactions:
        return {'interval': list(), 'dateValues': list()}
    else:
        today = date.fromisoformat('2023-05-20')
        beginning = sortedTransactions.first().purchaseDate
        interval = getInterval(beginning, today, timeInterval)
        dateValues = list()
        buttonLabelDates = [
            checkForPredates(beginning, today - relativedelta(years=1)),
            checkForPredates(beginning, today - relativedelta(months=6)),
            checkForPredates(beginning, today - relativedelta(months=1)),
            checkForPredates(beginning, today - relativedelta(weeks=1))
        ]
        buttonLabelValues = list()
        for IterDate in interval:
            dateVal = 0
            for thisAsset in sortedTransactions:
                if thisAsset.purchaseDate <= IterDate:
                    dateVal += thisAsset.amount * \
                        float(getAssetValue(thisAsset.asset, IterDate))
            print(IterDate)      
            if IterDate == beginning or IterDate in buttonLabelDates:
                print(IterDate)
                buttonLabelValues.append(dateVal)
                if IterDate == beginning and IterDate in buttonLabelDates:
                    count = buttonLabelDates.count(beginning)
                    for i in range (count):
                        buttonLabelValues.append(dateVal)
                
            if IterDate >= dateFrom:
                dateValues.append(dateVal)

        newButtonLabels = list()
        todaysVal = dateValues[-1]
        for labelVal in buttonLabelValues:
            label = round((todaysVal - labelVal)/labelVal*100, 2)
            if label >= 0:
                newButtonLabels.append(("+" + str(label) + "%"))
            else:
                newButtonLabels.append((str(label) + "%"))
                
        rightInterval = list(filter(lambda inter: inter >= dateFrom, interval))
        data = {'interval': rightInterval, 'dateValues': dateValues, 'buttonValues': newButtonLabels}
        return data

def createButtonVal(buttonLabelDates, buttonLabelValues, beginning):
    for buttonLabelDate in buttonLabelDates:
        if buttonLabelDate == beginning:
            buttonLabelValues

def checkForPredates(beginning, checkDate):
    if checkDate < beginning:
        return beginning
    else:
        return checkDate

def getInterval(beginning, today, interval):
    weeksList = list()
    iterDate = beginning
    while iterDate <= today:
        weeksList.append(iterDate)
        iterDate = iterDate + interval
    if today not in weeksList:
        weeksList.append(today)
    return weeksList


def getAssetValue(thisAsset, date):
    todaysHistory = AssetHistory.objects.get(name=thisAsset, date=date)
    currentVal = todaysHistory.value
    return currentVal


# TODO verschiedene Zeiträume für Wertverlauf anzeigen lassen
def asset(request, coin):
    selectedCoin = coin.upper()
    user = 1
    message = ""
    form = MyForm2(initial={'user': user, 'assetDropdown': selectedCoin})
    if request.method == 'POST':
        form = MyForm2(request.POST)
        if form.is_valid():
            message = addToPortfolio(form.cleaned_data)

    # TODO diesen Wert nehmen, wenn jeden Tag aktuelle Werte in die DB gespeichert werden
    # todaysValue = getCryptoValueFromDatabase(selectedCoin,datetime.today().strftime('%Y-%m-%d'))
    try:
        todaysValue = getCryptoValueFromDatabase(
            selectedCoin, datetime(2023, 4, 28))
    except:
        todaysValue = 0

    data = {'coinInfo': getCoinInformation(selectedCoin),
            'todaysValue': todaysValue,
            'values': getCryptoValuesFromDatabase(selectedCoin, date(year=2023, month=4, day=19), date(year=2023, month=5, day=16)),
            'form': form,
            'message': message}
    return render(request, 'dashboard_app/asset.html', context=data)


def addToPortfolio(cleanedData):
    if cleanedData.get('purchaseDate') > date.fromisoformat('2023-05-20'):
        return "You picked a date in the future!"
    date1 = cleanedData.get('purchaseDate')

    # print(cleanedData.get('assetDropdown'))

    if doesCoinExistInDatabase(cleanedData.get('assetDropdown')):
        asset = getAssetFromDatabase(cleanedData.get('assetDropdown'))
        user = getUser(cleanedData.get('user'))
        Transaction.objects.create(
            user=user,
            asset=asset,
            purchaseDate=datetime(date1.year, date1.month, date1.day),
            amount=cleanedData.get('amount')
        )
        return "Success: Asset saved"
    else:
        return "Error: Asset could not be saved"
