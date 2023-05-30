from django.db import models

from user_app.models import CustomUser


# Create your models here.


class Settings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # PortfolioSettings field's
    dateTimeFormat = models.CharField(
        max_length=30, blank=False, default="DD.MM.YYYY HH:mm")
    currency = models.CharField(max_length=30, blank=False, default="EUR")

    # NotificationSettings field's
    hasAssetAmountChanged = models.BooleanField(default=True)
    hasNewFollower = models.BooleanField(default=True)
    hasLikedPost = models.BooleanField(default=True)
    hasLikedComment = models.BooleanField(default=True)
    hasNewComment = models.BooleanField(default=True)
    hasSharedPost = models.BooleanField(default=True)

    # ViewSettings field's
    theme = models.CharField(max_length=30, blank=False, default="dark")

    def __str__(self):
        return self.user.username + "'s settings"
