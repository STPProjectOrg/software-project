
"""
This file contains all views for the notification_app.
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from notification_app.models import Notification


@login_required
def create_notification(request, notification_type, message):
    """
    Creates a notification.

    Keyword arguments:
        request (HttpRequest): The request object.
        notification_type (str): The type of the notification.
        message (str): The message of the notification.
    """

    notification = Notification.objects.get_or_create(
        user=request.user,
        notification_type=notification_type,
        message=message
    )[0]

    notification.save()


@login_required
def delete_notification(request, notification_id):
    """
    Deletes a notification.

    Keyword arguments:
        request (HttpRequest): The request object.
        notification_id (int): The id of the notification to be deleted.
    """

    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    return JsonResponse({"status": "success"})


@login_required
def delete_all_notifications(request):
    """
    Deletes all notifications for the user.

    Keyword arguments:
        request (HttpRequest): The request object.
    """

    notifications = Notification.objects.filter(user=request.user)
    notifications.delete()
    return JsonResponse({"status": "success"})


@login_required
def get_notifications(request):
    """
    Returns all notifications for the user.

    Keyword arguments:
        request (HttpRequest): The request object.
    """

    notifications = Notification.objects.filter(user=request.user)
    return JsonResponse({"notifications": notifications})


@login_required
def mark_notification_as_read(request, notification_id):
    """
    Marks a notification as read.

    Keyword arguments:
        request (HttpRequest): The request object.
        notification_id (int): The id of the notification to be marked as read.
    """

    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return JsonResponse({"status": "success"})


@login_required
def mark_all_notifications_as_read(request):
    """
    Marks all notifications as read.

    Keyword arguments:
        request (HttpRequest): The request object.
    """

    notifications = Notification.objects.filter(user=request.user)
    for notification in notifications:
        notification.read = True
        notification.save()
    return JsonResponse({"status": "success"})
