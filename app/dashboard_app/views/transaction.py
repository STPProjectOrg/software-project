""" view-functions related to dashboard_app.transaction """

# from datetime import datetime

from django.http import HttpResponseRedirect
from dashboard_app.models import Transaction
from dashboard_app.forms import TransactionBuyForm
from api_app.models import Asset


def buy(request):
    """ Create a new Transaction. """

    form = TransactionBuyForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data

        Transaction.objects.create(
            user=request.user,
            asset=Asset.objects.filter(name=form_data.get("asset")).get(),
            purchaseDate=form_data.get("date"),
            amount=form_data.get('amount')
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
