from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('', views.settings, name='overview'),
    path('userSettings/', views.userSettings, name='userSettings'),
    path('securitySettings/', views.securitySettings, name='securitySettings'),
    path('portfolioSettings/', views.portfolioSettings, name='portfolioSettings'),
    path('viewSettings/', views.viewSettings, name='viewSettings'),
    path('notificationSettings/', views.notificationSettings,
         name='notificationSettings'),
]
