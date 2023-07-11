""" view-functions related to dashboard_app.transaction """

# from datetime import datetime

from datetime import datetime
from django.http import HttpResponseRedirect
from dashboard_app.models import Transaction
from dashboard_app.forms import TransactionBuyForm
from api_app.models import Asset
from community_app.models import Post



def buy(request, coin):
    """ Create a new Transaction. """

    form = TransactionBuyForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        amount = form_data.get('amount')
        buyDate = form_data.get('date')
        buyCost= form_data.get('price') + form_data.get('tax') + form_data.get('charge')

        if(form_data.get('post') == True):
            Post.objects.create(
            user_id=request.user.id,
            content= 'Ich habe am '+ str(buyDate) + ' ' +str(amount) + ' ' + coin + ' für '+ str(buyCost)+ '€ gekauft ' + form_data.get("postText"),
            created_at=datetime.now(),
            tags=form_data.get("postText")
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
            cost= buyCost
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def sell(request, coin):
    """ Create a new Transaction. """

    form = TransactionBuyForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        amount = form_data.get('amount')
        buyDate = form_data.get('date')
        buyCost= -form_data.get('price') + form_data.get('tax') + form_data.get('charge')

        if(form_data.get('post') == True):
            Post.objects.create(
            user_id=request.user.id,
            content= 'Ich habe am '+ str(buyDate) + ' ' +str(amount) + ' ' + coin + ' für '+ str(buyCost)+ '€ verkauft ' + form_data.get("postText"),
            created_at=datetime.now(),
            tags=form_data.get("postText")
        )
        print(form_data.get("asset"))
        Transaction.objects.create(
            user=request.user,
            asset=Asset.objects.filter(name=coin).get(),
            purchaseDate=buyDate,
            amount= - amount,
            tax=form_data.get('tax'),
            charge=form_data.get('charge'),
            price= - form_data.get('price'),
            cost= buyCost
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
