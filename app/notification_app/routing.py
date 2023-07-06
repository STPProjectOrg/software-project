""" 
This file is used to route the websocket to the consumer.
"""

from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('notifications/<str:group_name>/', consumers.NotificationConsumer.as_asgi(),
         name='notificationService')
]
