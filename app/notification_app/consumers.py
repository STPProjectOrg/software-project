import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core import serializers

from user_app.models import CustomUser
from .models import Notification
from asgiref.sync import sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    This class represents a NotificationConsumer.
    """

    async def websocket_connect(self, message):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = str(self.scope["user"].pk)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            notifications = Notification.objects.afilter(
                user=self.scope["user"])
            notifications = await sync_to_async(
                serializers.serialize('json', notifications))

            await self.send(
                json.dumps({
                    "type": "websocket.connected",
                    "room": self.group_name,
                    "text": "Successfully connected to websocket.",
                    "notifications": notifications})
            )

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def websocket_receive(self, message):
        dddddd = database_sync_to_async(Notification.objects.create(
            user=self.scope["user"], type=message["type"], message=message["text"]))
        print(dddddd)
        await self.send(json.dumps({
            "type": "websocket.notification",
            "data": message
        }))

    async def send_notification(self, event):
        """
        This method is used to send a notification to the user.
        """

        await self.send(json.dumps({
            "type": "websocket.notification",
            "data": event
        }))
