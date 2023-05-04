from django.urls import re_path
from dashboard_app import views
app_name = 'dashboard_app'

urlpatterns = [
    re_path('dashboard', views.dashboard)
]