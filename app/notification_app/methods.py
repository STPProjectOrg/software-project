from channels.db import database_sync_to_async
from notification_app.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from user_app.models import CustomUser


@database_sync_to_async
def get_user(user_id):
    """
    This method is used to get a user.

    :param user_id: The primary key of the user.
    """
    return CustomUser.objects.get(pk=user_id)


@database_sync_to_async
def get_notifications(user_id):
    """
    This method is used to get a notification.

    :param notification_id: The primary key of the notification.
    """

    try:
        user = CustomUser.objects.get(pk=user_id)
        notifications = Notification.objects.filter(user=user)
    except (Notification.DoesNotExist):
        print("There where no notifications found.")
    return notifications


@database_sync_to_async
def create_notification(user_id, notification_type, message):
    """
    Creates a notification.

    :param user_id: The primary key of the user.
    :param notification_type: The type of the notification.
    :param message: The message of the notification.
    """
    user = CustomUser.objects.get(pk=user_id)

    notification = Notification.objects.create(
        user=user,
        type=notification_type,
        message=message
    )

    return notification


@database_sync_to_async
def delete_notification(notification_id):
    """
    Deletes a notification.

    :param notification_id: The primary key of the notification.
    """
    notification = Notification.objects.filter(id=notification_id)
    notification.delete()
    return notification


@database_sync_to_async
def delete_all_notifications(user_id):
    """
    Deletes all notifications for the user.

    :param user_id: The primary key of the user.
    """
    notifications = Notification.objects.filter(user=user_id)
    notifications.delete()
    return notifications


@database_sync_to_async
def mark_as_read(notification_id):
    """
    Marks a notification as read.

    :param notification_id: The primary key of the notification.
    """
    notification = Notification.objects.get(id=notification_id)
    notification.status = not notification.status
    notification.save()
    return notification


@database_sync_to_async
def mark_all_as_read(notification_id):
    """
    Marks all notifications as read.

    :param notification_id: The primary key of the notification.
    """

    notifications = Notification.objects.filter(user=notification_id)
    for notification in notifications:
        if notification.status is False:
            notification.status = not notification.status
            notification.save()
    return notifications


def send_notification(channel_layer, user_id, notification_type, message):
    """
    This method is used to send a notification to the user.

    :param user_id: The primary key of the user.
    :param notification_type: The type of the notification.
    :param message: The message of the notification.
    """

    async_to_sync(channel_layer.group_send)(
        f"{user_id}",
        {
            "type": "websocket.create_notification",
            "data": {
                "user": user_id,
                "type": notification_type,
                "message": message
            }
        }
    )
