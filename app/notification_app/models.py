"""
This file contains the models for the notification_app.
"""
from django.db import models

from user_app.models import CustomUser


class Notification(models.Model):
    """
    This class represents a notification.
    """

    NOTIFICATION_TYPES = (
        ('FOLLOWER', 'Wenn jemand ihnen folgt'),
        ('COMMENT', 'Wenn jemand ihren Beitrag kommentiert'),
        ('LIKE_POST', 'Wenn jemand ihren Beitrag liked'),
        ('LIKE_COMMENT', 'Wenn jemand ihren Kommentar liked'),
        ('COMMENT_ON_COMMENT', 'Wenn jemand ihren Kommentar kommentiert'),
        ('SHARE_POST', 'Wenn jemand ihren Beitrag teilt')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.notification_type}'
