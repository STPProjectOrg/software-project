from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from user_app.models import CustomUser, UserProfileInfo, UserFollowing
from user_app.forms import UserRegistrationForm, UserProfileInfoForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required


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
                  {'user_form':user_form, 
                   'profile_form':userprofile_form,
                   'registred':registred})



@login_required
def profile(request, username):

    # Check if the current profile is it's own profile or not an get the user from DB
    is_own_profile = False
    if username == "self":
        profile_user = CustomUser.objects.get(username=request.user.username)
        is_own_profile = True
    else:
        profile_user = get_object_or_404(CustomUser, username=username)

    # Get followers and following
    get_follower_count = profile_user.followers.count()
    get_following_count = profile_user.following.count()
    is_following = request.user.following.all().filter(following_user=profile_user).exists()

    # Get the picture url. When user doesn't have one get the default picture
    picture_url = profile_user.userprofileinfo.profile_pic.url if profile_user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"

    return render(request,'user_app/profile2.html', 
                  {"user_id": profile_user.id,
                   "user_profile_id": profile_user.userprofileinfo.id,
                   "user_name": profile_user.username,
                   "first_name": profile_user.first_name,
                   "last_name": profile_user.last_name,
                   "email": profile_user.email,
                   "picture_url": picture_url,
                   "is_own_profile": is_own_profile,
                   "followers": get_follower_count,
                   "following": get_following_count,
                   "is_following": is_following,
                   })

@login_required
def toggle_follow(request, username):
    profile_user = CustomUser.objects.get(username=request.user.username)
    other_user = get_object_or_404(CustomUser, username=username)
    
    if profile_user != other_user:
        if profile_user.following.all().filter(following_user=other_user).exists():
            UserFollowing.objects.filter(follower_user=profile_user, following_user=other_user).delete()
        else:
            UserFollowing.objects.create(follower_user=profile_user, following_user=other_user)

    return redirect(reverse('user_app:profile', kwargs={"username": username}))

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
    
def follower_list(request, username):
    profile_user = CustomUser.objects.get(username=username)
    follower_list = []
    for follower in UserFollowing.objects.filter(following_user_id=profile_user.id):
        username = CustomUser.objects.get(id=follower.follower_user_id).username
        followerData = {"username": username}
        follower_list.append(followerData)
    data = {"follower": follower_list}
    return  render(request,'user_app/follower_list.html', context=data)