from django.db import models
from api_app.models import Asset
from user_app.models import CustomUser

# Create your models here.
class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser ,on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    purchaseDate = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return self.asset
