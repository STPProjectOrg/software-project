from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, PasswordCustomResetForm, PasswordCustomSetForm
from .views import profile, auth, profile_edit

app_name = 'user_app'

urlpatterns = [
    # Loading and redirecting to profile page 
    path('profile-redirect/', profile.profile_redirect, name='profile_redirect'),
    path('profile/<str:username>/<int:timespan>/',
         profile.profile, name='profile'),

    # Following 
    path('follow/<str:username>', profile.toggle_follow, name='follow'),

    # Update Routes       
    path('update/userprofile/<int:pk>',
          profile_edit.ProfilePicUpdateView.as_view(), name='update_userprofile'),   
    path('update/userbanner/<int:pk>',
          profile_edit.ProfileBannerUpdateView.as_view(), name='update_userbanner'),
    path("update/biography", 
         profile_edit.BiographyUpdateView.as_view(), name="update_biography"),
    path('delete/userprofile/<int:pk>',
         profile_edit.delete_profile_pic, name='delete_userprofile'),

    # Registration
    path('register', auth.register, name='register'),
    path('register/success', auth.register_success, name='register_success'),

    # Auth
    path('login', auth_views.LoginView.as_view(
        template_name='user_app/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='core/landing.html'), name='logout'),

    # Password reset
    path('password-reset/',
         auth.ResetPasswordView.as_view(
             template_name="user_app/password_recovery/reset_password.html",
             form_class=PasswordCustomResetForm),
         name='reset_password'),
    path('password-reset-sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="user_app/password_recovery/reset_password_sent.html"),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth.ConfirmResetPasswordView.as_view(
             template_name="user_app/password_recovery/reset_password_confirm.html",
             form_class=PasswordCustomSetForm),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="user_app/password_recovery/reset_password_complete.html"),
         name='password_reset_complete'),
]
