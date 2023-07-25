""" view-functions related to community_app.comment """

from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from notification_app.methods.notification_methods import send_notification
from community_app.models import Comment, Post, CommentLike
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


def create(request, post_id):
    """
    Create a 'Comment' related to a given post.

    Keyword arguments:
        post_id: The id of the post to be commented.
    """
    post = Post.objects.filter(id=post_id).get()

    Comment.objects.create(
        user=request.user,
        post=post,
        content=request.POST.get("post_comment"),
        created_at=datetime.now()
    )

    send_notification(channel_layer, post.user.id, "comment",
                      f"{request.user.username} commented on your post.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete(request, comment_id):
    """
    Delete a 'Comment' by its id.

    Keyword arguments:
        id: The id of the 'Comment' to be deleted.
    """

    Comment.objects.filter(id=comment_id).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def like_comment(request, comment_id):
    """
    Toggles a 'CommentLikes' entrie by a given comment_id and the requesting user.

    Keyword arguments:
        comment_id: The id of the 'Comment' to be liked.
    """

    # Try deleting database entry
    try:
        CommentLike.objects.filter(
            user=request.user.id, comment=comment_id).get().delete()

    # Else create new entry
    except ObjectDoesNotExist:
        CommentLike.objects.create(user=request.user,
                                   comment=Comment.objects.get(id=comment_id))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
