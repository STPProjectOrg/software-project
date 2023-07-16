""" 
This file contains the models for the settings_app. 
"""

from django.db import models

from user_app.models import CustomUser


# Create your models here.


class Settings(models.Model):
    """
    This class represents the settings model.
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Portfoliosettings field's
    dateTimeFormat = models.CharField(
        max_length=30, blank=False, default="DD.MM.YYYY HH:mm")
    currency = models.CharField(max_length=30, blank=False, default="EUR")

    # Notificationsettings field's
    hasAssetAmountChanged = models.BooleanField(default=True)
    hasNewFollower = models.BooleanField(default=True)
    hasLikedPost = models.BooleanField(default=True)
    hasLikedComment = models.BooleanField(default=True)
    hasNewComment = models.BooleanField(default=True)
    hasSharedPost = models.BooleanField(default=True)

    #Post Settings
    posts_privacy_settings = models.CharField(max_length=10, default="all")

    # Watchlist Settings
    watchlist_privacy_settings = models.CharField(max_length=10, default="all")

    # Displaysettings field's
    theme = models.CharField(max_length=30, blank=False, default="dark")

    def __str__(self):
        return self.user.username + "'s settings"
