from django.urls import re_path, path
from community_app import views
app_name = 'community_app'

urlpatterns = [
    path('community/', views.community),
]