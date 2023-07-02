""" Main views for dashboard_app """

from django.db.models import Sum, F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api_app.models import Asset
from dashboard_app.views import charts
from dashboard_app.views import kpi
from dashboard_app.models import Watchlist
from dashboard_app.models import Transaction
from dashboard_app.views.watchlist import get_watchlist

# Create your views here.


@login_required
def dashboard(request, timespan):
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

    data = {
        "pie_data": charts.get_pie_data(assets),
        "line_data": charts.get_portfolio_line_data(transactions, timespan),
        "kpi": kpi.get_kpi(transactions, assets),
        "assets": assets}
    return render(request, 'dashboard_app/dashboard.html', data)


@login_required
def asset(request, name, timespan):
    """ Render an asset. """

    asset = Asset.objects.get(name=name)

    data = {"asset": asset,
            'asset_in_watchlist': Watchlist.objects.filter(user=request.user, asset=asset).exists(),
            "line_data": charts.get_asset_line_data(asset, timespan)}
    return render(request, 'dashboard_app/asset.html', data)


@login_required
def watchlist(request):

    data = {"watchlist": get_watchlist(request.user)}
    return render(request, 'dashboard_app/watchlist.html', context=data)


@login_required
def transactions(request):
    """ Render the transactions page. """

    data = {"transactions": Transaction.objects.filter(
        user=request.user.id).order_by("-purchaseDate")}

    return render(request, 'dashboard_app/transactions.html', context=data)
