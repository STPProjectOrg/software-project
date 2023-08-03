import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from user_app.models import CustomUser, UserProfileInfo, UserFollowing, ProfileBanner
from settings_app.models import Settings
from user_app.forms import UserRegistrationForm, UserLoginForm
from dashboard_app.views import charts
from api_app.models import Asset
from dashboard_app.models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.conf import settings
from django.db.models import Sum, F
from dashboard_app.views import kpi
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from community_app.views import post


# class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
#     template_name = 'users/password_reset.html'
#     email_template_name = "user_app/password_recovery/reset_password_email.html",
#     subject_template_name = "user_app/password_recovery/reset_password_email_subject",
#     success_url = reverse_lazy('user_app:password_reset_done')


# class ConfirmResetPasswordView(PasswordResetConfirmView):
#     success_url = reverse_lazy('user_app:password_reset_complete')

# Create your views here.


# def register(request):
#     registred = False

#     if request.method == "POST":
#         # Get the form data of the POST-method
#         user_form = UserRegistrationForm(data=request.POST)
#         userprofile_form = UserProfileInfoForm(data=request.POST)

#         if user_form.is_valid() and userprofile_form.is_valid():

#             # Save the user registration data from POST-form to the database and hash the password
#             new_user = user_form.save()
#             new_user.set_password(new_user.password)
#             new_user.save()

#             # Save the user-info registration data from POST-form to the database and connect them
#             # to the previous user table
#             new_profile = userprofile_form.save(commit=False)
#             new_profile.user = new_user
#             Settings.objects.get_or_create(user=new_user)

#             if 'profile_pic' in request.FILES:
#                 new_profile.profile_pic = request.FILES['profile_pic']
#             new_profile.save()

#             # Create new ProfileBanner instance 
#             ProfileBanner.objects.create(user=new_user)

#             registred = True
#             return render(request, 'user_app/register/registration_success.html')

#         print(user_form.errors, userprofile_form.errors)

#     else:
#         user_form = UserRegistrationForm()
#         userprofile_form = UserProfileInfoForm()

#     return render(request, 'user_app/register/registration.html',
#                   {'user_form': user_form,
#                    'profile_form': userprofile_form,
#                    'registred': registred})


# def register_success(request):
#     return render(request, 'user_app/register/registration_succsess.html')


# @login_required
# def profile_redirect(request):
#     username = request.user.username
#     profile_url = reverse('user_app:profile', kwargs={'username': username, 'timespan': 0})
#     return redirect(profile_url)


# @login_required
# def profile(request, username, timespan):
#     """ 
#     Render a user-profile.

#     Keyword arguments:
#         request: The http request
#         username: The profile user's username
#     """

#     # Get profile user
#     profile_user = get_object_or_404(
#         CustomUser.objects.select_related("userprofileinfo"), username=username)

#     # Declare common variables
#     user_following_list = request.user.following.values_list(
#         "following_user_id", flat=True)
#     is_user_profile = request.user.username == profile_user.username
#     is_user_following = profile_user.userprofileinfo.id in user_following_list

#     portfolio_privacy_setting = Settings.objects.get_or_create(user=profile_user)[0].dashboard_privacy_settings


#     # Get profile user's follow-lists
#     profile_followers_list = CustomUser.objects.filter(
#         following__following_user_id=profile_user.id).select_related("userprofileinfo")
#     profile_following_list = CustomUser.objects.filter(
#         followers__follower_user_id=profile_user.id).select_related("userprofileinfo")

#     # Post-Section
#     my_posts = post.get_by_user(profile_user)
#     postform = post.PostForm()

#     # Chart Data

#     transactions = Transaction.objects.filter(user=profile_user.id)
#     assets = Asset.objects.filter(transaction__user=profile_user.id).annotate(
#         amount=Sum("transaction__amount"),
#         cost=Sum("transaction__cost"),
#         total_value=F("amount") * F("price"),
#         profit=F("total_value") - F("cost")
#     ).distinct()

#     if not assets:
#         data = {"assets": None}

#     has_transactions = False
#     kpi_total = 0
    
#     if transactions:
#         kpi_total = kpi.get_kpi(transactions, assets)["total"]
#         has_transactions = True

#     if portfolio_privacy_setting == "without values":
#         kpi_total = 0
#         anonymize = True
#     else:
#         anonymize = False

#     return render(request, 'user_app/profile.html',
#                   {"profile_user": profile_user,
#                    'user_profile_id': profile_user.userprofileinfo.id,
#                    "is_user_profile": is_user_profile,
#                    "is_user_following": is_user_following,
#                    "portfolio_privacy_setting": portfolio_privacy_setting,
#                    "profile_followers_list": profile_followers_list,
#                    "profile_following_list": profile_following_list,
#                    "user_following_list": user_following_list,
#                    "postform": postform,
#                    "myposts": my_posts,
#                    "pie_data": charts.get_pie_data(assets, anonymize),
#                     "line_data": charts.get_portfolio_line_data(transactions, timespan, anonymize),
#                     "assets": assets,
#                     "kpi_total": kpi_total,
#                     "has_transactions":has_transactions,
#                    })


@login_required
def toggle_follow(request, username):
    profile_user = CustomUser.objects.get(username=request.user.username)
    other_user = get_object_or_404(CustomUser, username=username)

    if profile_user != other_user:
        if profile_user.following.all().filter(following_user=other_user).exists():
            UserFollowing.objects.filter(
                follower_user=profile_user, following_user=other_user).delete()
        else:
            UserFollowing.objects.create(
                follower_user=profile_user, following_user=other_user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def getUser(id):
    user = CustomUser.objects.get(id=id)
    return user


class ProfilePicUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfileInfo
    fields = ['profile_pic']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_app:profile_redirect')


class ProfileBannerUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfileInfo
    fields = ['profile_banner']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_app:profile_redirect')


@login_required
def update_user_profile_pic(request, pk):
    profile = UserProfileInfo.objects.get(id=pk)

    if request.method == 'POST':
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()

    return redirect(reverse('user_app:profile_redirect'))


@login_required
def update_user_profile_banner(request, pk):
    profile = ProfileBanner.objects.get(id=pk)

    if request.method == 'POST':
        new_banner = request.POST.get('profile_banner')
        
        # profile.profile_banner = getattr(ProfileBanner.BannerChoices, new_banner, None)
        profile.profile_banner = new_banner
        profile.save()
        # if 'profile_banner' in request.FILES:
        #     profile.profile_banner = request.FILES['profile_banner']
        #     profile.profile_pic = profile.profile_pic
        #     profile.save()

    return redirect(reverse('user_app:profile_redirect'))


@login_required
def delete_profile_pic(request, pk):
    user_profile = get_object_or_404(UserProfileInfo, pk=pk)

    if pk == request.user.userprofileinfo.id:
        user_profile.profile_pic.delete()
        # user_profile.delete_profile_pic()

    return redirect(reverse('user_app:profile_redirect'))


@login_required
def follower_list(request, username):
    profile_user = CustomUser.objects.get(username=username)
    follower_list = []
    for follower in UserFollowing.objects.filter(following_user_id=profile_user.id):
        follower_user = CustomUser.objects.get(id=follower.follower_user_id)
        is_following = UserFollowing.objects.filter(
            following_user_id=follower.follower_user.id).filter(follower_user_id=request.user.id).exists()
        followerData = {"username": follower_user.username, "user_picture": profile_user.userprofileinfo.get_profile_pic(),
                        "is_following": is_following, "followers": follower_user.followers.count()}
        follower_list.append(followerData)
    data = {"follower": follower_list}
    return render(request, 'user_app/follower_list.html', context=data)
