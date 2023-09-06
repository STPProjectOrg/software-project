""" 
This file contains all forms for the settings_app. 
"""

from django import forms

from user_app.models import CustomUser
from .models import Settings
from django.utils.translation import gettext_lazy as _

# TODO: Template String für Internationalisierung der Dropdown Texte
CHOICES = [(False, 'Deaktiviert'), (True, 'Aktiviert')]


class UserSettingsForm(forms.ModelForm):
    """
    This class represents the user settings form.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "id": "first_name",
        "class": "form-control",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "id": "last_name",
        "class": "form-control",
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "id": "username",
        "class": "form-control",
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "id": "email",
        "class": "form-control",
    }))

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]
        labels = {
            "username": _("Benutzername"),
            "email": _("Email"),
            "first_name": _("Vorname"),
            "last_name": _("Name")
        }


class PortfolioSettingsForm(forms.ModelForm):
    """
    This class represents the portfolio settings form.
    """
    date_format_choices = (
        ("DD.MM.YYYY HH:mm", "DD.MM.YYYY HH:mm"),
        ("MM/DD/YYYY HH:mm", "MM/DD/YYYY HH:mm"),
        ("YYYY-MM-DD HH:mm", "YYYY-MM-DD HH:mm")
    )

    dateTimeFormat = forms.ChoiceField(widget=forms.Select(
        attrs={
            "id": "dateTimeFormat",
            "class": "form-control"
        }),
        choices=date_format_choices)

    class Meta:
        model = Settings
        fields = ["dateTimeFormat", "currency", "theme"]


class NotificationSettingsForm(forms.ModelForm):
    hasAssetAmountChanged = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "id": "hasAssetAmountChanged",
        "role": "switch",
        "class": "form-check-input"
    }))
    hasNewFollower = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "id": "hasNewFollower",
        "role": "switch",
        "class": "form-check-input"
    }))
    hasLikedPost = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "id": "hasLikedPost",
        "role": "switch",
        "class": "form-check-input"
    }))
    hasLikedComment = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "id": "hasLikedComment",
        "role": "switch",
        "class": "form-check-input"
    }))
    hasNewComment = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "id": "hasNewComment",
        "role": "switch",
        "class": "form-check-input"
    }))
    hasSharedPost = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "id": "hasSharedPost",
        "role": "switch",
        "class": "form-check-input"
    }))

    """
    This class represents the notification settings form.
    """
    class Meta:
        model = Settings
        fields = ["hasAssetAmountChanged", "hasNewFollower", "hasLikedPost",
                  "hasLikedComment", "hasNewComment", "hasSharedPost"]


class SecuritySettingsForm(forms.Form):
    posts_privacy_setting = forms.CharField(label="Posts Privacy Setting", widget=forms.Select(
        choices=[("all", "all"), ("private", "private")],
        attrs={"class": "form-control",
               "id": "posts_privacy_setting"}),
        required=True)
    watchlist_privacy_setting = forms.CharField(label="Watchlist Privacy Setting", widget=forms.Select(
        choices=[("all", "all"), ("private", "private")],
        attrs={"class": "form-control",
               "id": "watchlist_privacy_setting"}),
        required=True)
    dashboard_privacy_setting = forms.CharField(label="Dashboard Privacy Setting", widget=forms.Select(
        choices=[(
            "all", "all"), ("without values", "without values"), ("private", "private")],
        attrs={"class": "form-control",
               "id": "dashboard_privacy_setting"}),
        required=True)

class LanguageSettingsForm(forms.Form):
    language_setting = forms.CharField(label="Language", widget=forms.Select(
        choices=[("de", "de"), ("en-us", "en-us")],
        attrs={"class": "form-control",
               "id": "language_setting"}),
        required=True)
