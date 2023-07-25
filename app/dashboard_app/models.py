from django.db import models
from django.db.models import F
from api_app.models import Asset
from user_app.models import CustomUser

class TransactionManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).annotate(
            invested=F('amount') * F('price')
        )

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
    objects = TransactionManager()

    def __str__(self):
        return self.asset

class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    privacy_settings = models.CharField(max_length=10, default="all")

class WatchlistAsset(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    added_at = models.DateTimeField()
    price_change = models.IntegerField(default=30)
