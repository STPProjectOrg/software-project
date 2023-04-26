
# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length= 50)
    password = models.CharField(max_length= 100)

class Asset(models.Model):
    assetname = models.CharField(max_length= 50)

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    amount = models.FloatField()
    buydate = models.DateTimeField("date bought")

class History(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateTimeField("value at date")