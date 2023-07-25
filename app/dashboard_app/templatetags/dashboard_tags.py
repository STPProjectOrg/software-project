""" Custom Tags for the dashboard_app """

from django import template
from dashboard_app.models import Transaction
from dashboard_app.forms import TransactionAddForm, TransactionUpdateForm

register = template.Library()


@register.inclusion_tag("dashboard_app/inclusion/line_chart.html")
def line_chart(chart_data):
    """ Include a line-chart element. """
    return {"data": chart_data["data"],
            "labels": chart_data["labels"]}


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


@register.inclusion_tag("dashboard_app/modals/transaction_add_modal.html")
def transaction_add_modal(user, asset, id):
    """ Include a modal for creating a buy-transaction. """

    return {"user": user, "asset": asset, "id": id, "form": TransactionAddForm()}


@register.inclusion_tag("dashboard_app/modals/transaction_update_modal.html")
def transaction_update_modal(transaction: Transaction):
    """ Include a modal for updating a transaction. """

    return {
        "form": TransactionUpdateForm(
            initial={"amount": transaction.amount,
                     "date": str(transaction.purchaseDate),
                     "price": transaction.price,
                     "charge": transaction.charge,
                     "tax": transaction.tax}),
        "transaction": transaction}


@register.inclusion_tag("dashboard_app/modals/transaction_delete_modal.html")
def transaction_delete_modal(id):
    """ Include a modal for deleteing a transaction. """

    return {"id": id}


@register.inclusion_tag("dashboard_app/inclusion/watchlist_asset.html")
def include_watchlist_asset(asset):
    """include KPI element"""
    return {"asset": asset}


@register.inclusion_tag("dashboard_app/inclusion/coin_overview_asset.html")
def include_coin_overview_asset(asset):
    """include KPI element"""
    return {"asset": asset}
