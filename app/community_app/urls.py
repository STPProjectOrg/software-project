from django.urls import path
from community_app.views import main, post, comment

app_name = 'community_app'

urlpatterns = [
    path('community/<str:feed>/', main.community, name="community"),
    path('community/<str:feed>/', main.toggle_feed, name='feed'),
    path('comment/delete/<int:comment_id>',
         comment.delete, name="comment_delete"),
    path('comment/add/<int:post_id>', comment.create, name="comment_create"),
    path('post/like/<int:post_id>', main.like_toggle, name="like_toggle"),
]
