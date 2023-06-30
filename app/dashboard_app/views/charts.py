from api_app.models import AssetManager
from dashboard_app.models import Asset


def get_pie_data(assets: AssetManager):
    """ Return suitable Chart.js pie data from a Asset QuerySet. """

    return {"data": list(assets.values_list("total_value", flat=True)),
            "labels": list(assets.values_list("coinName", flat=True)),
            "symbols": list(assets.values_list("name", flat=True))}


def get_portfolio_line_data():

    # return data?, labels?, button_values?
    # Button_values könnten dann nach bedarf genutzt werden und zum Beispiel in eine extra Komonente ausgelagert werden
    return None


def get_asset_line_data(asset: Asset):
    """
    Return data for an asset line chart.

    Keyword arguments:
        asset: The asset to be computed.
    """

    # return data?, labels?, button_values?
    # Button_values könnten dann nach bedarf genutzt werden und zum Beispiel in eine extra Komonente ausgelagert werden
    return None


def get_line_button_values(data, value):
    """
    Get Range-Selection values for a line-dataset.

    Keyword arguments:
        data: The line data.
        value: The current value.
    """

    return {"1-week": 0,
            "1-month": 0,
            "6-month": 0,
            "1-year": 0,
            "all": 0}
