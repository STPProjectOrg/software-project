import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from notification_app.methods.notification_methods import (
    create_notification,
    delete_all_notifications,
    delete_notification,
    get_notifications,
    mark_all_as_read,
    mark_as_read,
    switch_user_state
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
            await switch_user_state(self.group_name)
            await self.accept()

            await self.send(
                json.dumps({
                    "type": "websocket.connect",
                    "consumer": "notification_consumer",
                    "group": self.group_name,
                    "message": "Successfully connected to websocket."
                })
            )

            await self.channel_layer.group_send(
                f"{self.group_name}",
                {
                    "type": "websocket.all_notifications",
                    "consumer": "notification_consumer",
                }
            )

    async def websocket_receive(self, message):
        await self.send(
            json.dumps({
                "type": "websocket.receive",
                "consumer": "notification_consumer",
                "group": self.group_name,
                "message": "Received message."
            })
        )

        await self.channel_layer.group_send(
            f"{self.group_name}",
            {
                "type": "websocket.create_notification",
                "consumer": "notification_consumer",
                "message": message
            }
        )

    async def websocket_disconnect(self, message):
        await switch_user_state(self.group_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()

    async def websocket_all_notifications(self, message):
        """
        This method is used to get all notifications.
        """

        notifications = await get_notifications(self.group_name)
        parsed_notifications = {}

        async for notification in notifications:
            new_notification = {
                "id": notification.id,
                "type": notification.type,
                "message": notification.message,
                "status": notification.status,
                "created_at": notification.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            }
            parsed_notifications[notification.id] = new_notification

        await self.send(
            json.dumps({
                "type": "websocket.all_notifications",
                "consumer": "notification_consumer",
                "group": self.group_name,
                "notifications": parsed_notifications,
            })
        )

    async def websocket_create_notification(self, message):
        """
        This method is used to create a notification.
        """

        data = message.get("data")

        notification = await create_notification(
            data["user"],
            data["type"],
            data["message"]
        )

        await self.send(
            json.dumps({
                "type": "websocket.create_notification",
                "consumer": "notification_consumer",
                "group": self.group_name,
                "message": "Successfully created notification.",
                "notification_id": notification.id,
                "notification_type": notification.type,
                "notification_message": notification.message,
                "created_at": notification.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            })
        )

        await self.channel_layer.group_send(
            f"{data.get('user')}",
            {
                "type": "websocket.all_notifications",
                "consumer": "notification_consumer",
            }
        )

    async def websocket_delete_notification(self, message):
        """
        This method is used to delete a notification.
        """
        notification_id = message.get("notification_id")
        await delete_notification(notification_id)

        await self.send(
            json.dumps({
                "type": "websocket.delete_notification",
                "consumer": "notification_consumer",
                "group": self.group_name,
                "message": "Removed notification.",
            })
        )

        await self.channel_layer.group_send(
            f"{message['data'].get('user')}",
            {
                "type": "websocket.all_notifications",
                "consumer": "notification_consumer",
                "group": self.group_name,
            }
        )

    async def websocket_delete_all_notifications(self, message):
        """
        This method is used to delete all notifications.
        """
        await delete_all_notifications(self.group_name)

        await self.send(
            json.dumps({
                "type": "websocket.delete_all_notifications",
                "consumer": "notification_consumer",
                "group": self.group_name,
                "message": "Removed all notifications."
            })
        )

        await self.channel_layer.group_send(
            f"{self.group_name}",
            {
                "type": "websocket.all_notifications",
                "consumer": "notification_consumer",
                "group": self.group_name,
            }
        )

    async def websocket_mark_as_read(self, message):
        """
        This method is used to mark a notification as read.
        """

        notification_id = message.get("notification_id")
        await mark_as_read(notification_id)

        await self.send(
            json.dumps({
                "type": "websocket.mark_as_read",
                "consumer": "notification_consumer",
                "group": self.group_name,
                "message": "Marked notification as read.",
            })
        )

        await self.channel_layer.group_send(
            f"{self.group_name}",
            {
                "type": "websocket.all_notifications",
                "consumer": "notification_consumer",
                "group": self.group_name,
            }
        )

    async def websocket_mark_all_as_read(self, message):
        """
        This method is used to mark all notifications as read.
        """

        await mark_all_as_read(self.group_name)

        await self.send(
            json.dumps({
                "type": "websocket.mark_all_as_read",
                "consumer": "notification_consumer",
                "group": self.group_name,
                "message": "Marked all notifications as read.",
            })
        )

        await self.channel_layer.group_send(
            f"{self.group_name}",
            {
                "type": "websocket.notifications",
                "consumer": "notification_consumer",
            }
        )
