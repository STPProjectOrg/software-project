from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_app.models import CustomUser, UserProfileInfo
from django.contrib import messages
# Create your views here.


@login_required
def settings(request):
    return render(request, 'settings_app/settingsOverview.html')


@login_required
def userSettings(request):
    if request.method == "POST":
        user = CustomUser.objects.get(username=request.user.username)
        user_image = UserProfileInfo.objects.get(user=request.user)

        image_file = request.FILES.get('profile_pic', None)
        if image_file is not None:
            user_image.profile_pic = image_file
            user_image.user_profile.save()

        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]

        user.save()
        return render(request, 'settings_app/settingsOverview.html')
    else:
        return render(request, 'settings_app/userSettings.html')


@login_required
def securitySettings(request):
    return render(request, 'settings_app/securitySettings.html')


@login_required
def portfolioSettings(request):
    return render(request, 'settings_app/portfolioSettings.html')


@login_required
def notificationSettings(request):
    return render(request, 'settings_app/notificationSettings.html')


@login_required
def viewSettings(request):
    return render(request, 'settings_app/viewSettings.html')
