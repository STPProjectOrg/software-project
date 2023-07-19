""" 
This file is used to route the websocket to the consumer.
"""

from django.urls import path
from . import consumer


websocket_urlpatterns = [
    path('notifications/', consumer.NotificationConsumer.as_asgi(),
         name='notificationService')
]
