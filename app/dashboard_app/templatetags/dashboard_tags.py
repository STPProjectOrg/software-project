""" Custom Tags for the dashboard_app """

from django import template
from dashboard_app.forms import TransactionBuyForm

register = template.Library()


@register.inclusion_tag("dashboard_app/inclusion/line_chart.html")
def line_chart(chart_label):
    """ Include a line-chart element. """
    return {"chart_label": chart_label}


@register.inclusion_tag("dashboard_app/inclusion/pie_chart.html")
def pie_chart(pie_data):
    """ Include a pie-chart element. """
    return {"data": pie_data["data"],
            "labels": pie_data["labels"],
            "symbols": pie_data["symbols"]}


@register.inclusion_tag("dashboard_app/inclusion/include_chart.html")
def include_chart():
    """ Include Chart-JS. """
    return


@register.inclusion_tag("dashboard_app/inclusion/assets_table.html", takes_context=True)
def assets_table(context):
    """ Include a table overview of all assets in a given list. """
    return {"assets": context["assets"],
            "kpi": context["kpi"]}


@register.inclusion_tag("dashboard_app/modals/transaction_buy_modal.html")
def transaction_buy_modal(user, coinInfo):
    """ Include a modal for creating a buy-transaction. """

    return {"user": user, "coinInfo": coinInfo, "form": TransactionBuyForm()}


@register.inclusion_tag("dashboard_app/inclusion/watchlist_asset.html")
def include_watchlist_asset(asset):
    """include KPI element"""
    return {"asset": asset}
