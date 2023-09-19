
"""
This file contains all views for the settings app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_app.models import CustomUser
from .models import Settings
from .forms import NotificationSettingsForm, UserSettingsForm, SecuritySettingsForm, LanguageSettingsForm
from django.http import HttpResponseRedirect
from django.utils import translation
from community_app.models import Post
from dashboard_app.models import Watchlist
from app.settings import LANGUAGE_CODE


@login_required
def settings(request):
    """
    Renders the settings overview page.
    """
    return render(request, 'settings_app/settingsOverview.html', {"user": request.user})


@login_required
def user_settings(request):
    """
    Renders the user settings page.
    """
    user = CustomUser.objects.get(id=request.user.id)
    form = UserSettingsForm(instance=user)

    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
    return render(request, 'settings_app/userSettings.html', {'form': form})


@login_required
def security_settings(request):
    """
    Renders the security settings page.
    """
    settings = Settings.objects.get(user=request.user)
    form = SecuritySettingsForm(initial={"posts_privacy_setting": settings.posts_privacy_settings,
                                "watchlist_privacy_setting": settings.watchlist_privacy_settings, "dashboard_privacy_setting": settings.dashboard_privacy_settings})
    data = {"form": form}
    return render(request, 'settings_app/securitySettings.html', context=data)


@login_required
def security_settings_update(request):
    settings = Settings.objects.get_or_create(user=request.user)[0]
    form = SecuritySettingsForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        Settings.objects.filter(id=settings.id).update(posts_privacy_settings=form_data["posts_privacy_setting"], watchlist_privacy_settings=form_data[
            "watchlist_privacy_setting"], dashboard_privacy_settings=form_data["dashboard_privacy_setting"])
        Watchlist.objects.filter(user=request.user).update(
            privacy_settings=form_data["watchlist_privacy_setting"])
        Post.objects.filter(user=request.user).update(
            privacy_settings=form_data["posts_privacy_setting"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def portfolio_settings(request):
    """
    Renders the portfolio settings page.
    """

    if request.method == "POST":
        Settings.objects.filter(user=request.user).update(
            dateTimeFormat=request.POST["dateTimeFormat"],
            currency=request.POST["currencySelector"]
        )

    return render(request, 'settings_app/portfolioSettings.html')


@login_required
def notification_settings(request):
    """
    Renders the notification settings page.
    """
    setting = Settings.objects.get_or_create(user=request.user)[0]
    form = NotificationSettingsForm(
        initial={
            'hasAssetAmountChanged': setting.hasAssetAmountChanged,
            'hasNewFollower': setting.hasNewFollower,
            'hasLikedPost': setting.hasLikedPost,
            'hasLikedComment': setting.hasLikedComment,
            'hasNewComment': setting.hasNewComment,
            'hasSharedPost': setting.hasSharedPost
        })

    if request.method == "POST":
        form = NotificationSettingsForm(request.POST)
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
def view_settings(request):
    """
    Renders the view settings page.
    """
    form = LanguageSettingsForm(initial={"language": translation.get_language})
    data = {"form": form}
    if request.method == "POST":
        return HttpResponseRedirect("/i18n/setlang/en-us")
    return render(request, 'settings_app/viewSettings.html', context=data)
