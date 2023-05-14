from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm

app_name = 'user_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name = 'user_app/login.html', authentication_form = UserLoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name = 'core/landing.html'), name='logout'),
    path('profile/<str:username>/', views.profile, name='self_profile'),
    path('update/userprofile/<int:pk>', views.UserProfileUpdateView.as_view(), name='update_userprofile'),
]
'''
    path('<int:id>',include([
        path('update/', views.UserProfileUpdateView.as_view(), name='update_userprofile'),
    ]))
    '''