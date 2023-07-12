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
def get_notifications(pk):
    """
    This method is used to get notifications from a id.

    :param user: The user to get the notifications from.
    """
    try:
        notifications = Notification.objects.filter(id=pk).get()
    except (Notification.DoesNotExist):
        print("There where no notifications found.")
    finally:
        notifications = []
    return notifications


@database_sync_to_async
def create_notification(user, type, message):
    """
    Creates a notification.

    """
    notification = Notification.objects.get_or_create(
        user=user,
        type=type,
        message=message
    )[0]

    notification.save()


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
                f"{self.group_name}",
                {
                    "type": "websocket.notifications",
                }
            )

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def websocket_receive(self, message):
        await self.send(
            json.dumps({
                "type": "websocket.receive",
                "group": self.group_name,
                "message": "Received message."
            })
        )

        await self.channel_layer.group_send(
            f"{self.group_name}",
            {
                "type": "websocket.create_notification",
                "message": message
            }
        )

    async def websocket_create_notification(self, message):
        """
        This method is used to create a notification.
        """

        data = message.get("data")

        await create_notification(
            data["user"],
            data["type"],
            data["message"]
        )

        await self.send(
            json.dumps({
                "type": "websocket.create_notification",
                "group": self.group_name,
                "message": "Created notification."
            })
        )

        await self.channel_layer.group_send(
            f"{message['group']}",
            {
                "type": "websocket.notifications",
                "group": self.group_name,
            }
        )

    async def websocket_notifications(self):
        """
        This method is used to get all notifications.
        """

        notifications = await get_notifications(self.group_name)

        await self.send(
            json.dumps({
                "type": "websocket.notifications",
                "group": self.group_name,
                "notifications": notifications
            })
        )

        await self.channel_layer.group_send(
            f"{self.group_name}",
            {
                "notifications": notifications,
            }
        )

    async def send_notification(self, event):
        """
        This method is used to send a notification to the user.
        """

        await self.send(json.dumps({
            "type": "websocket.notification",
            "data": event
        }))
