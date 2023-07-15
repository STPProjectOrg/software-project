""" view-functions related to community_app.post """

from datetime import datetime

from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from community_app.models import Post, PostLike, Tag
from community_app.forms import PostForm
from messaging_app.utils import compress_image
from settings_app.models import Settings

def create(request):
    """ Create a new 'Post' from PostForm(). """
    settings = Settings.objects.get(user=request.user)
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        form_data = form.cleaned_data

        post = Post.objects.create(
            user_id=request.user.id,
            content=form_data.get("content"),
            created_at=datetime.now(),
            image = form_data.get("image"),
            tags=form_data.get("tags"),
            privacy_settings=settings.posts_privacy_settings
        )
        j = form_data.get("tags").split(",")
        for t in j:
            Tag.objects.get_or_create(tagname=t, post = post)
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

def get_by_tag(tag, **kwargs):
    tags = Tag.objects.filter(tagname=tag)
    posts = []
    for tag in tags:
        post = Post.objects.get(id=tag.post_id)
        posts.append(post)
    
    return posts

def get_by_user(user, **kwargs):
    posts = Post.objects.filter(user_id=user.id)
    return posts.order_by("-created_at")


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
