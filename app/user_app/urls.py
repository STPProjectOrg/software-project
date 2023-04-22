from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout')
]
