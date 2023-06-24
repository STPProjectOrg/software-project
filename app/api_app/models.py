from django.db import models

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    coinName = models.CharField(max_length=30, blank=False)
    imageUrl = models.URLField(blank=True)

    def __str__(self):
        return self.name
    
class AssetHistory(models.Model):
    date = models.DateField()
    value = models.FloatField(max_length=30, blank=False)
    name = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value)