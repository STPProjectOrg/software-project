from django.db import models
from django.db.models import F, Value, OuterRef, Subquery
from django.db.models.functions import FirstValue

class AssetManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        price_history_subquery = AssetHistory.objects.filter(name=OuterRef('pk')).order_by('-date')
        return super().get_queryset().annotate(
            price=Subquery(price_history_subquery.values('value')[:1]))

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    coinName = models.CharField(max_length=30, blank=False)
    imageUrl = models.URLField(blank=True)
    objects = AssetManager()

    def __str__(self):
        return self.name
    
class AssetHistory(models.Model):
    date = models.DateField()
    value = models.FloatField(max_length=30, blank=False)
    name = models.ForeignKey(Asset, on_delete=models.CASCADE)
    objects = models.Manager()
    

    def __str__(self):
        return str(self.value)
    
