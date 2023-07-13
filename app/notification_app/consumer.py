import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from notification_app.methods import (
    create_notification,
    delete_all_notifications,
    delete_notification,
    get_notifications,
    mark_all_as_read,
    mark_as_read
)


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

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()

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
                "message": "Created notification.",
            })
        )

        user = data["user"]

        await self.channel_layer.group_send(
            f"{user}",
            {
                "type": "websocket.notifications",
            }
        )

    async def websocket_notifications(self, message):
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

    async def delete_notification(self, message):
        """
        This method is used to delete a notification.
        """

        notification_id = message.get("id")
        removed_notification = await delete_notification(notification_id)

        await self.send(
            json.dumps({
                "type": "websocket.delete_notification",
                "group": self.group_name,
                "message": "Removed notification.",
                "notification": removed_notification
            })
        )

        await self.channel_layer.group_send(
            f"{message['group']}",
            {
                "type": "websocket.notifications",
                "group": self.group_name,
            }
        )

    async def delete_all_notifications(self, message):
        """
        This method is used to delete all notifications.
        """

        await delete_all_notifications(self.group_name)

        await self.send(
            json.dumps({
                "type": "websocket.delete_all_notifications",
                "group": self.group_name,
                "message": "Removed all notifications."
            })
        )

        await self.channel_layer.group_send(
            f"{message['group']}",
            {
                "type": "websocket.notifications",
                "group": self.group_name,
            }
        )

    async def mark_as_read(self, message):
        """
        This method is used to mark a notification as read.
        """

        notification_id = message.get("id")
        notification = await mark_as_read(notification_id)

        await self.send(
            json.dumps({
                "type": "websocket.mark_as_read",
                "group": self.group_name,
                "message": "Marked notification as read.",
                "notification": notification
            })
        )

        await self.channel_layer.group_send(
            f"{message['group']}",
            {
                "type": "websocket.notifications",
                "group": self.group_name,
            }
        )

    async def mark_all_as_read(self, message):
        """
        This method is used to mark all notifications as read.
        """

        notifications = await mark_all_as_read(self.group_name)

        await self.send(
            json.dumps({
                "type": "websocket.mark_all_as_read",
                "group": self.group_name,
                "message": "Marked all notifications as read.",
                "notifications": notifications
            })
        )

        await self.channel_layer.group_send(
            f"{message['group']}",
            {
                "type": "websocket.notifications",
            }
        )

    async def websocket_send_notification(self, message):
        """
        This method is used to send a notification to the user.
        """

        await self.channel_layer.group_send(
            f"{self.group_name}",
            {
                "type": "websocket.create_notification",
                "data": message.get("data")
            }
        )
