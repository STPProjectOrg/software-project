import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from user_app.models import CustomUser
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    This class represents a NotificationConsumer.
    """

    async def websocket_connect(self, message):
        # if self.scope["user"].is_anonymous:
        #     await self.close()
        # else:
        # self.group_name = str(self.scope["user"].pk)
        self.group_name = "test"  # der kann raus
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # notifications = await database_sync_to_async(Notification.objects.filter(user=self.scope["user"]))

        await self.send(
            json.dumps({
                "type": "websocket.connected",
                "text": "notifications"})
        )

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close()

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
