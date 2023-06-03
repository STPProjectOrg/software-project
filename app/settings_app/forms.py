""" 
This file contains all forms for the settings_app. 
"""

from django import forms

from user_app.models import CustomUser
from .models import Settings

# TODO: Template String für Internationalisierung der Dropdown Texte
CHOICES = [(False, 'Deaktiviert'), (True, 'Aktiviert')]


class UserSettingsForm(forms.ModelForm):
    """
    This class represents the user settings form.
    """
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]


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
            'hasAssetAmountChanged': "Benachrichtigung bei Veränderung der Assetmenge",
            'hasNewFollower': "Benachrichtigung wenn ihnen jemand folgt",
            'hasLikedPost': "Benachrichtigung wenn jemand einen ihrer Beiträge geliked hat",
            'hasLikedComment': "Benachrichtigung wenn jemand eins ihrer Kommentare geliked hat",
            'hasNewComment': "Benachrichtigung wenn jemand ein Kommentar"
            + "unter einem ihrer Beiträge verfasst hat",
            'hasSharedPost': "Benachrichtigung wenn jemand einen ihrer Beiträge geteilt hat"
        }
