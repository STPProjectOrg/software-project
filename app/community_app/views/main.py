""" Views for the community_app """

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from community_app.forms import PostForm
from community_app.models import Post, Like, Comment
from user_app.models import CustomUser, UserFollowing
from api_app.models import Asset


# Create your views here.


def posts_get(feed):
    """
    Get a filtered set of 'Posts'.

    Keyword arguments:
        feed: The feed to be filtered by.
        *args: The filter to be aplied.
        ** kwargs: The filter value.
    """

    match feed:
        case "all":
            return Post.objects.select_related("user_id", "user_id__userprofileinfo").order_by('-created_at')

        case "follower":
            return ""


def posts_create():
    ""


def posts_delete():
    ""


def like_toggle(request, post_id):
    """
    Toggles a 'PostLikes' entrie by a given post_id and the requesting user.

    Keyword arguments:
        post_id: The id of the 'Post' to be toggled.
    """

    # Try deleting database entry
    try:
        Like.objects.filter(
            user_id=request.user.id, post_id=post_id).get().delete()

    # Else create new entry
    except ObjectDoesNotExist:
        Like.objects.create(user_id=request.user,
                            post_id=Post.objects.get(id=post_id)
                            )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def community(request, feed):
    # selectedCoin = 'BTC'
    # user = 1
    form = PostForm(initial={'user_id': request.user.id})
    if request.method == 'POST':
        if 'comment' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                d = form.cleaned_data
                user = CustomUser.objects.get(id=request.user.id)
                post = Post.objects.create(
                    user_id=user,                    content=d.get("content"),
                    created_at=datetime.now(),
                    tags=d.get("tags")
                )
    # if request.GET.get("comment_id") is not None:
    #     PostComments.objects.filter(id=request.GET.get("comment_id")).delete()
    # if request.GET.get('post_id') is not None:
    #     if request.GET.get('post_comment') is not None and request.GET.get("post_comment") != "":
    #         Comment.objects.create(
    #             user_id=CustomUser.objects.get(id=request.user.id),
    #             post_id=Post.objects.get(id=request.GET.get('post_id')),
    #             content=request.GET.get('post_comment'),
    #             created_at=datetime.now()
    #         )
    #     elif request.GET.get('post_id') is not None:
    #         post_id = request.GET.get('post_id')
    #         if Like.objects.filter(user_id=request.user.id, post_id=post_id).exists():
    #             Like.objects.filter(
    #                 user_id=request.user.id, post_id=post_id).delete()
    #         else:
    #             Like.objects.create(
    #                 user_id=CustomUser.objects.get(id=request.user.id),
    #                 post_id=Post.objects.get(id=post_id)
    #             )

    if feed == "all":
        posts = posts_get(feed)
    elif feed == "follower":
        posts = []
        f = UserFollowing.objects.all().filter(follower_user_id=request.user.id)
        for follow in f:
            po = Post.objects.all().filter(user_id=follow.following_user_id)
            for p in po:
                posts.append(p)
        posts = reversed(convertPosts(posts))
    else:
        posts = Post.objects.all().filter(user_id=request.user.id)
        posts = reversed(convertPosts(posts))

    user_picture = request.user.userprofileinfo.profile_pic.url if request.user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
    data = {'user': request.user,
            "user_picture": user_picture,
            'form': form,
            'posts': posts,
            'all': 'all',
            'follower': 'follower',
            'feed': feed}
    return render(request, 'community_app/community.html', context=data)


def toggle_feed(request, feed):
    return redirect(reverse('community_app:community', kwargs={"feed": feed}))


def convertPosts(posts):
    convertedPosts = []
    for post in posts:
        user = CustomUser.objects.get(id=post.user_id.id)
        username = user.username
        asset = Asset.objects.get(name=post.asset.name).name
        post = Post.objects.get(id=post.id)
        post_id = Post.objects.get(id=post.id).id
        content = post.content
        created_at = post.created_at
        hashtags = post.hashtags
        likes = Like.objects.filter(post_id=post).count()
        comments = convertComments(post_id)
        picture = user.userprofileinfo.profile_pic.url if user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        postObject = {"username": username,
                      "asset": asset,
                      "content": content,
                      "created_at": created_at,
                      "hashtags": hashtags,
                      "likes": likes,
                      "post_id": post_id,
                      "comments": comments,
                      "commentsLength": comments.__len__(),
                      "picture": picture}
        convertedPosts.append(postObject)
    return convertedPosts


def convertComments(post_id):
    convertedComments = []
    for comment in Comment.objects.filter(post_id=post_id):
        id = comment.id
        user = CustomUser.objects.get(id=comment.user_id.id)
        content = comment.content
        created_at = comment.created_at
        picture = user.userprofileinfo.profile_pic.url if user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        commentObject = {"id": id, "user": user, "user_picture": picture,
                         "content": content, "created_at": created_at}
        convertedComments.append(commentObject)
    return convertedComments
