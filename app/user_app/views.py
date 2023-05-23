from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from user_app.models import CustomUser, UserProfileInfo, UserFollowing
from user_app.forms import UserRegistrationForm, UserProfileInfoForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = "user_app/password_recovery/reset_password_email.html",
    subject_template_name = "user_app/password_recovery/reset_password_email_subject",
    success_url = reverse_lazy('user_app:password_reset_done')


class ConfirmResetPasswordView(PasswordResetConfirmView):
    success_url = reverse_lazy('user_app:password_reset_complete')

# Create your views here.


def register(request):
    registred = False

    if request.method == "POST":
        # Get the form data of the POST-method
        user_form = UserRegistrationForm(data=request.POST)
        userprofile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():

            # Save the user registration data from POST-form to the database and hash the password
            new_user = user_form.save()
            new_user.set_password(new_user.password)
            new_user.save()

            # Save the user-info registration data from POST-form to the database and connect them
            # to the previous user table
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user

            if 'profile_pic' in request.FILES:
                new_profile.profile_pic = request.FILES['profile_pic']
            new_profile.save()

            registred = True
            return redirect(reverse('core:index'))

        else:
            print(user_form.errors, userprofile_form.errors)

    else:
        user_form = UserRegistrationForm()
        userprofile_form = UserProfileInfoForm()

    return render(request, 'user_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': userprofile_form,
                   'registred': registred})


@login_required
def profile_redirect(request):
    username = request.user.username
    profile_url = reverse('user_app:profile', kwargs={'username': username})
    return redirect(profile_url)


@login_required
def profile(request, username):

    # Check if the current profile is it's own profile or not an get the user from DB
    profile_user = get_object_or_404(
        CustomUser, username=username)
    is_own_profile = request.user.username == profile_user.username

    # following_list = CustomUser.objects.filter(id=1)
    followers = CustomUser.objects.filter(
        following__following_user_id=profile_user.id).select_related("userprofileinfo")
    following = CustomUser.objects.filter(
        followers__follower_user_id=profile_user.id).select_related("userprofileinfo")

    own_following = request.user.following.values_list(
        "following_user_id", flat=True)

    # is_followig und picture_url direct im Objekt speichern
    is_following = request.user.following.all().filter(
        following_user=profile_user).exists()
    picture_url = profile_user.userprofileinfo.profile_pic.url if profile_user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"

    # Get the picture url. When user doesn't have one get the default picture

    return render(request, 'user_app/profile.html',
                  {"profile_user": profile_user,
                   "user_profile_id": profile_user.userprofileinfo.id,
                   "picture_url": picture_url,
                   "is_own_profile": is_own_profile,
                   "is_following": is_following,
                   "followers": followers,
                   "following": following,
                   "own_following": own_following,
                   })


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


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfileInfo
    fields = ['profile_pic']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_app:profile', kwargs={"username": "self"})


@login_required
def follower_list(request, username):
    profile_user = CustomUser.objects.get(username=username)
    follower_list = []
    for follower in UserFollowing.objects.filter(following_user_id=profile_user.id):
        follower_user = CustomUser.objects.get(id=follower.follower_user_id)
        user_picture = profile_user.userprofileinfo.profile_pic.url if profile_user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        is_following = UserFollowing.objects.filter(
            following_user_id=follower.follower_user.id).filter(follower_user_id=request.user.id).exists()
        followerData = {"username": follower_user.username, "user_picture": user_picture,
                        "is_following": is_following, "followers": follower_user.followers.count()}
        follower_list.append(followerData)
    data = {"follower": follower_list}
    return render(request, 'user_app/follower_list.html', context=data)
