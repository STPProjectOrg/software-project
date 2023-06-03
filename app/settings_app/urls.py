""" 
This module defines the URL patterns for the settings_app app.
"""

from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('', views.settings, name='overview'),
    path('userSettings/', views.user_settings, name='userSettings'),
    path('securitySettings/', views.security_settings, name='securitySettings'),
    path('portfolioSettings/', views.portfolio_settings, name='portfolioSettings'),
    path('viewSettings/', views.view_settings, name='viewSettings'),
    path('notificationSettings/', views.notification_settings,
         name='notificationSettings'),
]
