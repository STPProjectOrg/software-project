""" Models for the core_app """

# Create your models here.
from django.db import models
from user_app.models import CustomUser


class Asset(models.Model):
    assetname = models.CharField(max_length=50)


class Receipt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    amount = models.FloatField()
    buydate = models.DateTimeField("date bought")


class History(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateTimeField("value at date")
