from django.shortcuts import render
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
            form = PostForm(request.POST)
            if form.is_valid():
                d = form.cleaned_data
                user = CustomUser.objects.get(id=request.user.id)
                post = Posts.objects.create(
                    user_id= user,
                    asset=Asset.objects.get(name=d.get("asset")),
                    content=d.get("content"),
                    created_at=datetime.now(),
                    hashtags=d.get("hashtags")
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
        elif request.GET.get('post_id') is not None:
            post_id = request.GET.get('post_id')
            if PostLikes.objects.filter(user_id=request.user.id, post_id=post_id).exists():
                PostLikes.objects.filter(user_id=request.user.id, post_id=post_id).delete()
            else:
                PostLikes.objects.create(
                    user_id = CustomUser.objects.get(id=request.user.id),
                    post_id = Posts.objects.get(id=post_id)
                    )


    posts = Posts.objects.all()
    posts = reversed(convertPosts(posts))
    user_picture = request.user.userprofileinfo.profile_pic.url if request.user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
    data = {'user': request.user, "user_picture": user_picture, 'form': form, 'posts': posts}
    return render(request, 'community_app/community.html' ,context=data)

def convertPosts(posts):
    convertedPosts = []
    for post in posts:
        user = CustomUser.objects.get(id=post.user_id.id)
        username = user.username
        asset = Asset.objects.get(name=post.asset.name).name
        post = Posts.objects.get(id=post.id)
        post_id = Posts.objects.get(id=post.id).id
        content = post.content
        created_at = post.created_at
        hashtags = post.hashtags
        likes = PostLikes.objects.filter(post_id = post).count()
        comments = convertComments(post_id)
        picture = user.userprofileinfo.profile_pic.url if user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        postObject = {"username":username, 
                      "asset":asset, 
                      "content":content, 
                      "created_at":created_at, 
                      "hashtags":hashtags, 
                      "likes": likes, 
                      "post_id": post_id, 
                      "comments": comments, 
                      "commentsLength": comments.__len__(),
                      "picture": picture}
        convertedPosts.append(postObject)
    return convertedPosts

def convertComments(post_id):
    convertedComments = []
    for comment in PostComments.objects.filter(post_id=post_id):
        id = comment.id
        user = CustomUser.objects.get(id=comment.user_id.id)
        content = comment.content
        created_at = comment.created_at
        picture = user.userprofileinfo.profile_pic.url if user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        commentObject = {"id":id, "user": user, "user_picture": picture, "content": content, "created_at": created_at}
        convertedComments.append(commentObject)
    return convertedComments
