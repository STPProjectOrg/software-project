""" Views for the community_app """


from django.shortcuts import render
from community_app.forms import PostForm
from community_app.views import post


# Create your views here.

def community(request, feed):
    """
    Render the community page.

    Keyword arguments:
        feed: The feed to be displayed.    
    """

    form = PostForm()
    posts = post.get_by_feed(feed, user_id=request.user.id)
    
    data = {
        'form': form,
        'posts': posts
    }

    return render(request, 'community_app/community.html', context=data)
