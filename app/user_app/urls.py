from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views_old
from .forms import UserLoginForm, PasswordCustomResetForm, PasswordCustomSetForm
from .views import biography, profile

app_name = 'user_app'

urlpatterns = [
    # Loading and redirecting to profile page 
    path('profile-redirect/', profile.profile_redirect, name='profile_redirect'),
    path('profile/<str:username>/<int:timespan>/',
         profile.profile, name='profile'),
         
    path('update/userprofile/<int:pk>',
         views_old.update_user_profile_pic, name='update_userprofile'),
    path('update/userbanner/<int:pk>',
         views_old.update_user_profile_banner, name='update_userbanner'),
    #     path('update/userprofile/<int:pk>',
    #          views.ProfilePicUpdateView.as_view(), name='update_userprofile'),
    #     path('update/userbanner/<int:pk>',
    #          views.ProfileBannerUpdateView.as_view(), name='update_userbanner'),
    path('delete/userprofile/<int:pk>',
         views_old.delete_profile_pic, name='delete_userprofile'),
    path('follow/<str:username>', views_old.toggle_follow, name='follow'),
    path('follower_list/<str:username>',
         views_old.follower_list, name='follower_list'),

    # Registration
    path('register', views_old.register, name='register'),
    path('register/success', views_old.register_success, name='register_success'),

    # Auth
    path('login', auth_views.LoginView.as_view(
        template_name='user_app/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='core/landing.html'), name='logout'),

    # Password reset
    path('password-reset/',
         views_old.ResetPasswordView.as_view(
             template_name="user_app/password_recovery/reset_password.html",
             form_class=PasswordCustomResetForm),
         name='reset_password'),
    path('password-reset-sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="user_app/password_recovery/reset_password_sent.html"),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         views_old.ConfirmResetPasswordView.as_view(
             template_name="user_app/password_recovery/reset_password_confirm.html",
             form_class=PasswordCustomSetForm),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="user_app/password_recovery/reset_password_complete.html"),
         name='password_reset_complete'),

    # Update User Information
    path('update/biography', biography.update, name='update_biography'),

]
