""" view-functions related to community_app.comment """

from datetime import datetime
from django.http import HttpResponseRedirect
from community_app.models import Comment, Post


def create(request, post_id):
    """
    Create a 'Comment' related to a given post.

    Keyword arguments:
        post_id: The id of the post to be commented.
    """

    Comment.objects.create(
        user=request.user,
        post=Post.objects.filter(id=post_id).get(),
        content=request.POST.get("post_comment"),
        created_at=datetime.now()
    )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete(request, comment_id):
    """
    Delete a 'Comment' by its id.

    Keyword arguments:
        id: The id of the 'Comment' to be deleted.
    """

    Comment.objects.filter(id=comment_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
