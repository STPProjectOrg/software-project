from django.db.models import F, Subquery
from api_app.models import Asset, AssetManager, AssetHistory
from dashboard_app.models import TransactionManager, Transaction
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


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


def get_asset_line_data(asset: Asset):
    """
    Return data for an asset line chart.

    Keyword arguments:
        asset: The asset to be computed.
    """

    # return data?, labels?, button_values?
    # Button_values könnten dann nach bedarf genutzt werden und zum Beispiel in eine extra Komonente ausgelagert werden
    return None


def get_line_button_values(data):
    """
    Get range-selection values for a line-dataset.

    Keyword arguments:
        data: The line data.
    """

    value = data[-1:][0]

    return {"1week": (value - data[-7:][0]) / data[-7:][0],
            "1month": (value - data[-31:][0]) / data[-31:][0],
            "6month": (value - data[-186:][0]) / data[-186:][0],
            "1year": (value - data[-365:][0]) / data[-365:][0],
            "all": (value - data[0]) / data[0]}
