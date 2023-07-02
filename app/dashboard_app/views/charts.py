from datetime import date, timedelta
from django.db.models import F, Subquery
from api_app.models import Asset, AssetManager, AssetHistory
from dashboard_app.models import TransactionManager, Transaction


def get_pie_data(assets: AssetManager):
    """ Return suitable Chart.js pie data from a Asset QuerySet. """

    return {"data": list(assets.values_list("total_value", flat=True)),
            "labels": list(assets.values_list("coinName", flat=True)),
            "symbols": list(assets.values_list("name", flat=True))}


def get_portfolio_line_data(transactions: TransactionManager, timespan: int):
    """ Return data for a portfolio line chart based on a given transaction QuerySet. """

    data = []
    labels = []
    today = date.fromisoformat('2023-05-20')  # TODO: ANPASSEN!
    day = transactions.earliest('purchaseDate').purchaseDate

    while day <= today:

        # Get the assets held by the user on the current day
        assets = transactions.filter(
            purchaseDate__lte=day).values('asset').distinct()

        # Calculate the value for the current day
        value = sum(
            Transaction.objects.filter(asset=asset['asset'], purchaseDate__lte=day).annotate(
                invested=F('amount') *
                Subquery(
                    AssetHistory.objects.filter(
                        name=asset['asset'], date=day).values('value')[:1]
                )
            ).values('invested')[0]['invested']
            for asset in assets
        )

        data.append(value)
        labels.append(day.strftime("%d.%m.%Y"))

        day += timedelta(days=1)

    return {"button_values": get_line_button_values(data),
            "data": data[-timespan:],
            "labels": labels[-timespan:]}


def get_asset_line_data(asset: Asset, timespan: int):
    """
    Return data for an asset line chart.

    Keyword arguments:
        asset: The asset to be computed.
    """

    data = []
    labels = []

    history = AssetHistory.objects.filter(name=asset).order_by("date")
    day = history.earliest("date").date
    latest = history.latest("date").date

    while day <= latest:

        # Calculate the value for the current day
        value = history.filter(date=day).values("value")[0]['value']

        data.append(value)
        labels.append(day.strftime("%d.%m.%Y"))

        day += timedelta(days=1)

    return {"button_values": get_line_button_values(data),
            "data": data[-timespan:],
            "labels": labels[-timespan:]}


def get_line_button_values(data):
    """
    Get range-selection values for a line-dataset.

    Keyword arguments:
        data: The line data.
    """

    def calc_growth(start, end):
        return (end - start) / start

    return {"1week": calc_growth(data[-7:][0], data[-1:][0]),
            "1month": calc_growth(data[-31:][0], data[-1:][0]),
            "6month": calc_growth(data[-186:][0], data[-1:][0]),
            "1year": calc_growth(data[-365:][0], data[-1:][0]),
            "all": calc_growth(data[0], data[-1:][0])}
