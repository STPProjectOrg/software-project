from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from community_app.forms import PostForm
from community_app.models import Posts, PostLikes, PostComments
from user_app.models import CustomUser
from api_app.models import Asset
from datetime import datetime
# Create your views here.
def community(request):
    selectedCoin = 'BTC'
    user = 1
    form = PostForm(initial={'user_id': user, 'asset': selectedCoin})
    if request.method=='POST':
        if 'comment' in request.POST:
            print("comment")
            form = PostForm(request.POST)
            print(form)
            if form.is_valid():
                d = form.cleaned_data
                user = CustomUser.objects.get(id=request.user.id)
                post = Posts.objects.create(
                    user_id= user,
                    asset=Asset.objects.get(name=d.get("asset")),
                    content=d.get("content"),
                    created_at=d.get("created_at"),
                    hashtags=d.get("hashtags")
                )
                postLikes = PostLikes.objects.create(
                    user_id = user,
                    post_id = post
                )

    if request.GET.get("comment_id") is not None:
        PostComments.objects.filter(id=request.GET.get("comment_id")).delete()

    if request.GET.get('post_id') is not None:
        if request.GET.get('post_comment') is not None and request.GET.get("post_comment") != "":
            PostComments.objects.create(
                user_id = CustomUser.objects.get(id=request.user.id),
                post_id = Posts.objects.get(id=request.GET.get('post_id')),
                content = request.GET.get('post_comment'), 
                created_at = datetime.now()
            )
        post_id = request.GET.get('post_id')
        if PostLikes.objects.filter(user_id=request.user.id, post_id=post_id).exists():
            PostLikes.objects.filter(user_id=request.user.id, post_id=post_id).delete()
        else:
            PostLikes.objects.create(
                user_id = CustomUser.objects.get(id=request.user.id),
                post_id = Posts.objects.get(id=post_id)
                )


    posts = Posts.objects.all()
    posts = convertPosts(posts)
    data = {'user': request.user.username, 'form': form, 'posts': posts}
    return render(request, 'community_app/community.html' ,context=data)

def abc(request, userid, postid):
    print(f"{userid} + + {postid}")
    return HttpResponse()

def convertPosts(posts):
    convertedPosts = []
    for post in posts:
        user = CustomUser.objects.get(id=post.user_id.id).username
        asset = Asset.objects.get(name=post.asset.name).name
        post = Posts.objects.get(id=post.id)
        post_id = Posts.objects.get(id=post.id).id
        content = post.content
        created_at = post.created_at
        hashtags = post.hashtags
        likes = PostLikes.objects.filter(post_id = post).count()
        comments = convertedComments(post_id)
        postObject = {"user":user, "asset":asset, "content":content, "created_at":created_at, "hashtags":hashtags, "likes": likes, "post_id": post_id, "comments": comments, "commentsLength": comments.__len__()}
        convertedPosts.append(postObject)
    return convertedPosts

def convertedComments(post_id):
    convertedComments = []
    for comment in PostComments.objects.filter(post_id=post_id):
        id = comment.id
        user = CustomUser.objects.get(id=comment.user_id.id).username
        content = comment.content
        created_at = comment.created_at
        commentObject = {"id":id, "user": user, "content": content, "created_at": created_at}
        convertedComments.append(commentObject)
    return convertedComments
