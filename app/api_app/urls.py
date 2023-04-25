from django.urls import re_path
from api_app import views
app_name = 'api_app'

urlpatterns = [
    re_path('api', views.api)
]