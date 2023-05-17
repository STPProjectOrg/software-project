from django.urls import re_path
from community_app import views
app_name = 'community_app'

urlpatterns = [
    re_path('community', views.community),
]