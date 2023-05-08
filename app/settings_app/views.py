from django.shortcuts import render

# Create your views here.


def settings(request):
    return render(request, 'settings_app/settingsOverview.html')


def userSettings(request):
    return render(request, 'settings_app/userSettings.html')


def securitySettings(request):
    return render(request, 'settings_app/securitySettings.html')


def portfolioSettings(request):
    return render(request, 'settings_app/portfolioSettings.html')


def notificationSettings(request):
    return render(request, 'settings_app/notificationSettings.html')


def viewSettings(request):
    return render(request, 'settings_app/viewSettings.html')
