from django.db import models

from user_app.models import CustomUser


# Create your models here.


class Settings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Portfoliosettings field's
    dateTimeFormat = models.CharField(
        max_length=30, blank=False, default="DD.MM.YYYY HH:mm")
    currency = models.CharField(max_length=30, blank=False, default="EUR")

    # Notificationsettings field's
    assetAmountChanged = models.BooleanField(blank=False, default=False)
    followMessage = models.BooleanField(blank=False, default=True)
    likedPostMessage = models.BooleanField(blank=False, default=True)
    likedCommentMessage = models.BooleanField(blank=False, default=True)
    commentedMessage = models.BooleanField(blank=False, default=True)
    sharedPostMessage = models.BooleanField(blank=False, default=False)
    changedIpAdress = models.BooleanField(blank=False, default=False)

    # Displaysettings field's
    theme = models.CharField(max_length=30, blank=False, default="dark")

    def __str__(self):
        return self.user.username + "'s settings"
