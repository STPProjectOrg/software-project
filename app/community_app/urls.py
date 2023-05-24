from django.urls import path
from community_app import views
app_name = 'community_app'

urlpatterns = [
    path('community/<str:feed>/', views.community, name="community"),
    path('community/<str:feed>/', views.toggle_feed, name='feed'),
]