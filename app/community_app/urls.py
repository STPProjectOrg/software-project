""" Routes for the community_app """

from django.urls import path
from community_app.views import main, post, comment

app_name = 'community_app'

urlpatterns = [
    # Main
    path('community/<str:feed>/', main.community, name="community"),

    # Comment
    path('comment/add/<int:post_id>', comment.create, name="comment_create"),
    path('comment/like/<int:comment_id>', comment.like_comment, name="like_comment"),
    path('comment/delete/<int:comment_id>',
         comment.delete, name="comment_delete"),

    # Post
    path('post/like/<int:post_id>', post.like_toggle, name="like_toggle"),
    path('post/create', post.create, name="post_create"),
    path('post/delete/<int:post_id>', post.delete, name="post_delete"),
]
