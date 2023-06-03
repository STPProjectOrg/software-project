"""
This file contains the models for the notification_app.
"""
from django.db import models

from app.user_app.models import CustomUser


class Notification(models.Model):
    """
    This class represents the notification model.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Notification field's
    type = models.CharField(max_length=30, blank=False, default="like")
    message = models.CharField(max_length=30, blank=False, default="like")
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + "'s notification"
