""" view-functions related to dashboard_app.transaction """

# from datetime import datetime

from datetime import datetime
from django.http import HttpResponseRedirect
from dashboard_app.models import Transaction
from dashboard_app.forms import TransactionAddForm
from api_app.models import Asset
from community_app.models import Post


def add(request, coin):
    """ Create a new Transaction. """

    form = TransactionAddForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        sell = form_data.get('sell')
        amount = form_data.get('amount')
        buyDate = form_data.get('date')
        price = form_data.get('price')
        message = 'gekauft'
        if sell:
            amount = -amount
            price = -price
            message = 'verkauft'
        buyCost =  price + \
            form_data.get('tax') + form_data.get('charge')

        if (form_data.get('post') == True):
            Post.objects.create(
                user_id=request.user.id,
                content='Ich habe am ' + str(buyDate) + ' ' + str(amount) + ' ' + coin + ' für ' + str(
                    buyCost) + '€ ' + message + ' ' + form_data.get("postText"),
                created_at=datetime.now(),
                tags=form_data.get("tags")
            )
        print(form_data.get("asset"))
        Transaction.objects.create(
            user=request.user,
            asset=Asset.objects.filter(name=coin).get(),
            purchaseDate=buyDate,
            amount=amount,
            tax=form_data.get('tax'),
            charge=form_data.get('charge'),
            price=form_data.get('price'),
            cost=buyCost
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete(request, transaction_id):
    """ Delete an transaction by its id. """

    transaction = Transaction.objects.get(id=transaction_id)
    transaction.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update(request, transaction_id):
    Transaction.objects.filter(id=transaction_id).update(
        price=request.POST["price"],
        purchaseDate=request.POST["date"],
        amount=request.POST["amount"],
        charge=request.POST["charge"],
        tax=request.POST["tax"],
        cost=(float(request.POST["price"]) + float(request.POST["charge"]) + float(request.POST["tax"])))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
