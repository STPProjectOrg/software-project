""" 
This file is used to route the websocket to the consumer.
"""

from django.urls import path
from .consumers import notification_consumer, chat_consumer


websocket_urlpatterns = [
    path('notifications/', notification_consumer.NotificationConsumer.as_asgi(),
         name='notificationService'),
    path('chat/', chat_consumer.ChatConsumer.as_asgi(),
         name='chatService')

]
