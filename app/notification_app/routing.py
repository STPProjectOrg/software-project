""" 
This file is used to route the websocket to the consumer.
"""

from django.urls import path
from .consumers import notification_consumer


websocket_urlpatterns = [
    path('notifications/', notification_consumer.NotificationConsumer.as_asgi(),
         name='notificationService')
]
