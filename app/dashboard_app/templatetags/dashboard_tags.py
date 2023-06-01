""" Custom Tags for the dashboard_app """

from django import template
from dashboard_app.forms import TransactionBuyForm

register = template.Library()


@register.inclusion_tag("dashboard_app/inclusion/line_chart.html")
def line_chart(chart_label):
    """ Include a line-chart element. """
    return {"chart_label": chart_label}


@register.inclusion_tag("dashboard_app/inclusion/pie_chart.html")
def pie_chart():
    """ Include a line-chart element. """
    return


@register.inclusion_tag("dashboard_app/inclusion/include_chart.html")
def include_chart():
    """ Include Chart-JS. """
    return


@register.inclusion_tag("dashboard_app/modals/transaction_buy_modal.html")
def transaction_buy_modal(user, coin):
    """ Include a modal for creating a buy-transaction. """

    return {"user": user, "coin": coin, "form": TransactionBuyForm()}
