"""
This file contains the models for the notification_app.
"""
from django.db import models

from user_app.models import CustomUser


class Notification(models.Model):
    """
    This class represents a notification.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    type = models.TextField(default="", max_length=20)
    message = models.TextField(default="")
    status = models.CharField(default="UNREAD", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.type}'
