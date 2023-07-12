from channels.db import database_sync_to_async
from notification_app.models import Notification

from user_app.models import CustomUser


@database_sync_to_async
def get_user(user_id):
    """
    This method is used to get a user.

    :param user_id: The primary key of the user.
    """
    return CustomUser.objects.get(pk=user_id)


@database_sync_to_async
def get_notifications(notification_id):
    """
    This method is used to get a notification.

    :param notification_id: The primary key of the notification.
    """

    try:
        notifications = Notification.objects.filter(id=notification_id).get()
    except (Notification.DoesNotExist):
        print("There where no notifications found.")
    finally:
        notifications = []
    return notifications


@database_sync_to_async
def create_notification(user_id, notification_type, message):
    """
    Creates a notification.

    :param user_id: The primary key of the user.
    :param notification_type: The type of the notification.
    :param message: The message of the notification.
    """

    notification = Notification.objects.get_or_create(
        user=user_id,
        type=notification_type,
        message=message
    )[0]

    notification.save()
    return notification


@database_sync_to_async
def delete_notification(notification_id):
    """
    Deletes a notification.

    :param notification_id: The primary key of the notification.
    """
    notification = Notification.objects.get(id=notification_id)
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
        notification.status = not notification.status
        notification.save()
    return notifications
