""" Main views for dashboard_app """

from datetime import datetime, date, timedelta
from django.db.models import Sum, F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api_app.models import Asset, AssetHistory
from api_app.views import (getAssetFromDatabase, doesCoinExistInDatabase,
                           getCoinInformation, getCryptoValuesFromDatabase)
import dashboard_app.views.charts as chart
from user_app.views import getUser
from dateutil.relativedelta import relativedelta
from dashboard_app.models import Watchlist
from dashboard_app.models import Transaction
from dashboard_app.views.watchlist import get_watchlist

# Create your views here.


@login_required
def view_dashboard(request):
    """ Render the dashboard. """

    # get querysets
    transactions = Transaction.objects.filter(user=request.user.id)
    assets = Asset.objects.filter(transaction__user=request.user).annotate(
        amount=Sum("transaction__amount"),
        cost=Sum("transaction__cost"),
        total_value=F("amount") * F("price"),
        profit=F("total_value") - F("cost")
    ).distinct()

    if not assets:
        data = {"assets": None}
        return render(request, "dashboard_app/dashboard.html", data)

    today = date.fromisoformat('2023-05-20')

    if 'complete' in request.POST:
        chartData = getDataForLine(
            request.user, date.min, relativedelta(days=1))
    else:
        if 'month' in request.POST:
            chartData = getDataForLine(
                request.user, today - relativedelta(months=1), relativedelta(days=1))
        else:
            if 'week' in request.POST:
                chartData = getDataForLine(
                    request.user, today - timedelta(days=7), relativedelta(days=1))
            else:
                if 'sixmonths' in request.POST:
                    chartData = getDataForLine(
                        request.user, today - relativedelta(months=6), relativedelta(days=1))
                else:
                    if 'year' in request.POST:
                        chartData = getDataForLine(
                            request.user, today - relativedelta(years=1), relativedelta(days=1))
                    else:
                        chartData = getDataForLine(
                            request.user, date.min, relativedelta(days=1))

    # get chart data
    line_data = None

    data = {
        "pie_data": chart.get_pie_data(assets),
        **chartData,
        "line_data": chart.get_portfolio_line_data(transactions, 7),
        "kpi": get_kpi(transactions, assets),
        "assets": assets}
    return render(request, 'dashboard_app/dashboard.html', data)


def get_kpi(transactions, assets):
    """ Return the key performce indicators for a given user's profile. """

    invested = transactions.aggregate(Sum("price"))["price__sum"]
    tax = transactions.aggregate(Sum("tax"))["tax__sum"]
    charge = transactions.aggregate(Sum("charge"))["charge__sum"]
    total = assets.aggregate(Sum('total_value'))['total_value__sum']
    cost = invested + tax + charge
    profit = total - cost

    return {"invested": invested,
            "tax": tax,
            "charge": charge,
            "total": total,
            "cost": cost,
            "profit": profit}


@login_required
def view_asset(request, name):
    """ Render an asset. """

    asset = Asset.objects.get(name=name)

    data = {"asset": asset,
            'asset_in_watchlist': Watchlist.objects.filter(user=request.user, asset=asset).exists(),
            "line_data": chart.get_asset_line_data(asset)}
    return render(request, 'dashboard_app/asset.html', context=data)


def getDataForLine(user, dateFrom, timeInterval):
    sortedTransactions = Transaction.objects.filter(
        user=user.id).order_by('purchaseDate')
    if not sortedTransactions:
        return {'interval': list(), 'dateValues': list()}
    else:
        today = date.fromisoformat('2023-05-20')
        beginning = sortedTransactions.first().purchaseDate
        interval = get_interval(beginning, today, timeInterval)
        dateValues = list()
        buttonLabelDates = [
            check_predates(beginning, today - relativedelta(years=1)),
            check_predates(beginning, today - relativedelta(months=6)),
            check_predates(beginning, today - relativedelta(months=1)),
            check_predates(beginning, today - relativedelta(weeks=1))
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
                    for i in range(count):
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
        data = {'interval': rightInterval, 'dateValues': dateValues,
                'buttonValues': newButtonLabels, 'totalValue': round(dateValues[-1], 2)}
        return data


def check_predates(start, date):
    return start if date < start else date


def get_interval(start, today, interval):
    weeks = []
    while start <= today:
        weeks.append(start)
        start = start + interval
    if today not in weeks:
        weeks.append(today)
    return weeks


def getAssetValue(thisAsset, date):
    todaysHistory = AssetHistory.objects.get(name=thisAsset, date=date)
    currentVal = todaysHistory.value
    return currentVal


@login_required
def watchlist(request):

    data = {"watchlist": get_watchlist(request.user)}
    return render(request, 'dashboard_app/watchlist.html', context=data)


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
