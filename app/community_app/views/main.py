""" Views for the community_app """


from django.shortcuts import render
from community_app.forms import PostForm
from community_app.views import post
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def community(request, feed):
    """
    Render the community page.

    Keyword arguments:
        feed: The feed to be displayed.    
    """

    form = PostForm()
    if feed == "all" or feed == "follower":
        posts = post.get_by_feed(feed, user_id=request.user.id)
    else:
        posts = post.get_by_tag(feed)

    data = {
        'form': form,
        'posts': posts
    }

    return render(request, 'community_app/community.html', context=data)

