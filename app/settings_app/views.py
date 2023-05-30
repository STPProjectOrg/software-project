from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import notificationSettingsForm
from user_app.models import CustomUser, UserProfileInfo
from .models import Settings
from django.contrib import messages
# Create your views here.


@login_required
def settings(request):
    return render(request, 'settings_app/settingsOverview.html')


@login_required
def userSettings(request):
    if request.method == "POST":
        user = CustomUser.objects.get(username=request.user.username)

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
    if request.method == "POST":
        # Do something with the request
        return render(request, 'settings_app/settingsOverview.html')
    else:
        return render(request, 'settings_app/securitySettings.html')


@login_required
def portfolioSettings(request):
    if request.method == "POST":
        setting = Settings.objects.get_or_create(user=request.user)

        setting.dateTimeFormat = request.POST["dateTimeFormat"]
        setting.currency = request.POST["currencySelector"]
        setting.save()

        return render(request, 'settings_app/settingsOverview.html')
    else:
        return render(request, 'settings_app/portfolioSettings.html')


@login_required
def notificationSettings(request):
    setting = Settings.objects.get_or_create(user=request.user)[0]
    form = notificationSettingsForm(
        initial={
            'hasAssetAmountChanged': setting.hasAssetAmountChanged,
            'hasNewFollower': setting.hasNewFollower,
            'hasLikedPost': setting.hasLikedPost,
            'hasLikedComment': setting.hasLikedComment,
            'hasNewComment': setting.hasNewComment,
            'hasSharedPost': setting.hasSharedPost
        })

    if request.method == "POST":
        form = notificationSettingsForm(request.POST)
        if form.is_valid():
            setting.hasAssetAmountChanged = form.cleaned_data["hasAssetAmountChanged"]
            setting.hasNewFollower = form.cleaned_data["hasNewFollower"]
            setting.hasLikedPost = form.cleaned_data["hasLikedPost"]
            setting.hasLikedComment = form.cleaned_data["hasLikedComment"]
            setting.hasNewComment = form.cleaned_data["hasNewComment"]
            setting.hasSharedPost = form.cleaned_data["hasSharedPost"]

            setting.save()

    return render(request, 'settings_app/notificationSettings.html', {'form': form})


@login_required
def viewSettings(request):
    return render(request, 'settings_app/viewSettings.html')
