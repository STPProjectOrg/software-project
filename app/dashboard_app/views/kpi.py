from django.db.models import Sum


def get_kpi(transactions, assets):
    """ Return the key performce indicators for a given user's profile. """

    invested = transactions.aggregate(Sum("price"))["price__sum"]
    tax = transactions.aggregate(Sum("tax"))["tax__sum"]
    charge = transactions.aggregate(Sum("charge"))["charge__sum"]
    total = assets.aggregate(Sum('total_value'))['total_value__sum']
    cost = invested + tax + charge
    profit = total - cost

    return {"invested": invested,
            "tax": tax,
            "charge": charge,
            "total": total,
            "cost": cost,
            "profit": profit}
