from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm, PasswordCustomResetForm, PasswordCustomSetForm

app_name = 'user_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name = 'user_app/login.html', authentication_form = UserLoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name = 'core/landing.html'), name='logout'),
    path('profile-redirect/', views.profile_redirect, name='profile_redirect'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('update/userprofile/<int:pk>', views.UserProfileUpdateView.as_view(), name='update_userprofile'),
    path('follow/<str:username>', views.toggle_follow, name='follow'),
  path('follower_list/<str:username>', views.follower_list, name='follower_list'),
    
    # Password reset
    path('password-reset/',
        views.ResetPasswordView.as_view(
        template_name="user_app/password_recovery/reset_password.html", 
        form_class = PasswordCustomResetForm), 
        name='reset_password'),
    path('password-reset-sent/',
        auth_views.PasswordResetDoneView.as_view(
        template_name="user_app/password_recovery/reset_password_sent.html"), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        views.ConfirmResetPasswordView.as_view(
        template_name="user_app/password_recovery/reset_password_confirm.html", 
        form_class = PasswordCustomSetForm), 
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
        template_name="user_app/password_recovery/reset_password_complete.html"), 
        name='password_reset_complete')
]

