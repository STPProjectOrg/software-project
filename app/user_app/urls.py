from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm

app_name = 'user_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name = 'user_app/login.html', authentication_form = UserLoginForm), name='login'),
    # path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('profile', views.self_profile, name='self_profile')
]
