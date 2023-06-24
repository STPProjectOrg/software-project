from django.db import models
from api_app.models import Asset
from user_app.models import CustomUser

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser ,on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    purchaseDate = models.DateField()
    amount = models.FloatField()
    price = models.FloatField()
    tax = models.FloatField()
    charge = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return self.asset

class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    added_at = models.DateTimeField()
    price_change = models.IntegerField(default=30)