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
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]
        labels = {
            "username": _("Benutzername"),
            "email": _("Email"),
            "first_name": _("Vorname"),
            "last_name": _("Name")
            }
        

class PortfolioSettingsForm(forms.Form):
    """
    This class represents the portfolio settings form.
    """
    class Meta:
        model = Settings
        fields = ["dateTimeFormat", "currency", "theme"]

class NotificationSettingsForm(forms.ModelForm):
    """
    This class represents the notification settings form.
    """
    class Meta:
        model = Settings
        fields = ["hasAssetAmountChanged", "hasNewFollower", "hasLikedPost",
                  "hasLikedComment", "hasNewComment", "hasSharedPost"]
        labels = {
            'hasAssetAmountChanged': _("Benachrichtigung bei Veränderung der Assetmenge"),
            'hasNewFollower': _("Benachrichtigung wenn ihnen jemand folgt"),
            'hasLikedPost': _("Benachrichtigung wenn jemand einen ihrer Beiträge geliked hat"),
            'hasLikedComment': _("Benachrichtigung wenn jemand eins ihrer Kommentare geliked hat"),
            'hasNewComment': _("Benachrichtigung wenn jemand ein Kommentar von dir kommentiert"),
            'hasSharedPost': _("Benachrichtigung wenn jemand einen ihrer Beiträge geteilt hat")
        }

class SecuritySettingsForm(forms.Form):
    posts_privacy_setting = forms.CharField(label="Posts Privacy Setting",widget=forms.Select(choices=[("all","all"),("private","private")], attrs={"class": "form-control"}), required=True)
    watchlist_privacy_setting = forms.CharField(label="Watchlist Privacy Setting",widget=forms.Select(choices=[("all","all"),("private","private")], attrs={"class": "form-control"}), required=True)