from django.db import models

from user_app.models import CustomUser


# Create your models here.


class Settings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dateTimeFormat = models.CharField(
        max_length=30, blank=False, default="DD.MM.YYYY HH:mm")
    currency = models.CharField(max_length=30, blank=False, default="EUR")
    theme = models.CharField(max_length=30, blank=False, default="dark")

    def __str__(self):
        return self.user.username + "'s settings"
