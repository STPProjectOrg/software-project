from django.shortcuts import render
from community_app.forms import PostForm, LikeForm
from community_app.models import Posts, PostLikes, PostComments
from user_app.models import CustomUser
from api_app.models import Asset
# Create your views here.
def community(request):
    selectedCoin = 'BTC'
    user = 1
    message = ""
    form = PostForm(initial={'user_id': user, 'asset': selectedCoin})
    likeForm = LikeForm(initial={'user_id': user})
    if request.method=='POST':
        if 'comment' in request.POST:
            print("comment")
            form = PostForm(request.POST)
            print(form)
            if form.is_valid():
                d = form.cleaned_data
                user = CustomUser.objects.get(id=d.get("user_id"))
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
        elif 'like' in request.POST:
            print("like")
            print("METHOD: POST")
            likeForm = LikeForm(request.POST)
            print(request.POST)
            print(likeForm)                
            if form.is_valid():
                d = form.cleaned_data
                print("IN")
                PostLikes.objects.create(
                    user_id = CustomUser.objects.get(id=d.get("user_id")),
                    post_id = Posts.objects.get(id=d.get("post_id"))
                    )


    posts = Posts.objects.all()
    posts = convertPosts(posts)
    data = {'value': 0, 'form': form, 'likeForm': likeForm, 'posts': posts}
    return render(request, 'community_app/community.html' ,context=data)

def convertPosts(posts):
    convertedPosts = []
    for post in posts:
        user = CustomUser.objects.get(id=post.user_id.id).username
        asset = Asset.objects.get(name=post.asset.name).name
        content = post.content
        created_at = post.created_at
        hashtags = post.hashtags
        postObject = {"user":user, "asset":asset, "content":content, "created_at":created_at, "hashtags":hashtags}
        convertedPosts.append(postObject)
    return convertedPosts