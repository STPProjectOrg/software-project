from django.db import models

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    coinName = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.name
    
class AssetHistory(models.Model):
    date = models.DateField(unique=True)
    value = models.CharField(max_length=30, blank=False)
    name = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return self.value