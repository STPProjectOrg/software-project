""" view-functions related to community_app.post """

from datetime import datetime

from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from community_app.models import Post, PostLike
from community_app.forms import PostForm


def create(request):
    """ Create a new 'Post' from PostForm(). """

    form = PostForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        Post.objects.create(
            user_id=request.user.id,
            content=form_data.get("content"),
            created_at=datetime.now(),
            tags=form_data.get("tags")
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete(request, post_id):
    """
    Delete a 'Post' by its id.

    Keyword arguments:
        id: The id of the 'Post' to be deleted.
    """

    Post.objects.filter(id=post_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_by_feed(feed, **kwargs):
    """
    Get a filtered set of 'Posts'.

    Keyword arguments:
        feed: The feed to be filtered by.
        ** kwargs: The filter values.
    """

    posts = Post.objects.select_related("user", "user__userprofileinfo")
    posts = posts.order_by("-created_at")

    match feed:
        case "follower":
            posts = posts.filter(
                user_id__followers__follower_user_id=kwargs.get("user_id"))

        case "personal":
            posts.filter(user_id=kwargs.get("user_id"))

    return posts


def like_toggle(request, post_id):
    """
    Toggles a 'PostLikes' entrie by a given post_id and the requesting user.

    Keyword arguments:
        post_id: The id of the 'Post' to be toggled.
    """

    # Try deleting database entry
    try:
        PostLike.objects.filter(
            user=request.user.id, post=post_id).get().delete()

    # Else create new entry
    except ObjectDoesNotExist:
        PostLike.objects.create(user=request.user,
                                post=Post.objects.get(id=post_id))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
