from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from user_app.models import CustomUser
from user_app.forms import UserForm, UserProfileInfoForm, UserLoginForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    registred = False

    if request.method == "POST":
        # Get the form data of the POST-method
        user_form = UserForm(data=request.POST)
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
        user_form = UserForm()
        userprofile_form = UserProfileInfoForm()

    return render(request, 'user_app/registration.html', 
                  {'user_form':user_form, 
                   'profile_form':userprofile_form,
                   'registred':registred})


def user_login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(data=request.POST)

        username = login_form.username         #request.POST.get('username')
        password = login_form.password         #request.POST.get('password')
        current_user = authenticate(username=username, password=password)

        if current_user:
            login(request,current_user)
            return redirect(reverse('core:index'))
            '''
            if current_user.is_active:
                login(request,current_user)
                return redirect(reverse('core:index'))
            else:
                return HttpResponse("Account not active")
            '''
        else: 
            print("Someone tried to login and failed")
            login_form.add_error(None, 'Invalid Login Details!')
            # return HttpResponse("Invalid login details")
    else:
        login_form = UserLoginForm()
    
    return render(request,'user_app/login.html',{'login_form':login_form})
    

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('core:index'))

@login_required
def self_profile(request):
    user = get_object_or_404(CustomUser, username=request.user.username)
    picture_url = user.userprofileinfo.profile_pic.url if user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
    return render(request,'user_app/profile.html', 
                  {"user_name": user.username,
                   "first_name": user.first_name,
                   "last_name": user.last_name,
                   "email": user.email,
                   "picture_url": picture_url})

def getUser(id):
    user = CustomUser.objects.get(id=id)
    return user