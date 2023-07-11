import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core import serializers

from user_app.models import CustomUser
from .models import Notification
from asgiref.sync import sync_to_async


@database_sync_to_async
def get_user(pk):
    """
    This method is used to get a user.

    :param pk: The primary key of the user.
    """
    return CustomUser.objects.get(pk=pk)


@database_sync_to_async
def get_notifications(user):
    """
    This method is used to get notifications from a user.

    :param user: The user to get the notifications from.
    """
    try:
        notifications = Notification.objects.filter(user=user).get()
    except (Notification.DoesNotExist):
        print("There where no notifications found.")
    finally:
        notifications = []
    return notifications


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

            await self.send(
                json.dumps({
                    "type": "websocket.connect",
                    "group": self.group_name,
                    "message": "Successfully connected to websocket."
                })
            )

            await self.channel_layer.group_send(
                "%s" % self.group_name,
                {
                    "type": "websocket.initial_notifications",
                }
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
