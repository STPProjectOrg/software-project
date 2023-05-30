from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import notificationSettingsForm, portfolioSettingsForm, userSettingsForm, viewSettingsForm
from user_app.models import CustomUser, UserProfileInfo
from .models import Settings
from django.contrib import messages
# Create your views here.


@login_required
def settings(request):
    Settings.objects.get_or_create(id=request.user.id)
    return render(request, 'settings_app/settingsOverview.html')


@login_required
def userSettings(request):
    user = CustomUser.objects.get(id=request.user.id)
    form = userSettingsForm(instance=user)

    if request.method == "POST":
        form = userSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    return render(request, 'settings_app/userSettings.html', {'form': form})


@login_required
def securitySettings(request):
    return render(request, 'settings_app/securitySettings.html')


@login_required
def portfolioSettings(request):
    setting = Settings.objects.get(id=request.user.id)
    form = portfolioSettingsForm(instance=setting)

    if request.method == "POST":
        form = portfolioSettingsForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()

    return render(request, 'settings_app/portfolioSettings.html', {'form': form})


@login_required
def notificationSettings(request):
    setting = Settings.objects.get(id=request.user.id)
    form = notificationSettingsForm(instance=setting)

    if request.method == "POST":
        form = notificationSettingsForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()

    return render(request, 'settings_app/notificationSettings.html', {'form': form})


@login_required
def viewSettings(request):
    setting = Settings.objects.get(id=request.user.id)
    form = viewSettingsForm(instance=setting)

    if request.method == "POST":
        form = viewSettingsForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()

    return render(request, 'settings_app/viewSettings.html', {'form': form})
