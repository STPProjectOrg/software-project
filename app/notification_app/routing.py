""" 
This file is used to route the websocket to the consumer.
"""

from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('notifications/', consumers.NotificationConsumer.as_asgi(),
         name='notificationService')
]
