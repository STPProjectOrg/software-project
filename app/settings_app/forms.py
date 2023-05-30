from django import forms

from user_app.models import CustomUser
from .models import Settings

CHOICES = [(True, "Ja"), (False, "Nein")]


class userSettingsForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]


class portfolioSettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ["dateTimeFormat", "currency"]
        labels = {"dateTimeFormat": "Datumsformat",
                  "currency": "Währung"}
        widgets = {
            "dateTimeFormat": forms.Select(choices=[(1, "DD.MM.YYYY HH:mm"), (2, "MM/DD/YYYY HH:mm"), (3, "YYYY-MM-DD HH:mm")]),
            "currency": forms.Select(choices=[(1, "EUR"), (2, "USD"), (3, "GBP"), (4, "Yen")]),
        }


class viewSettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ["theme"]
        labels = {"theme": "Theme"}
        widgets = {
            "theme": forms.Select(choices=[(1, "Dunkel"), (2, "Hell")])
        }


class notificationSettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ["hasAssetAmountChanged", "hasNewFollower", "hasLikedPost",
                  "hasLikedComment", "hasNewComment", "hasSharedPost"]
        labels = {
            'hasAssetAmountChanged': "Benachrichtigung bei Veränderung der Assetmenge",
            'hasNewFollower': "Benachrichtigung wenn ihnen jemand folgt",
            'hasLikedPost': "Benachrichtigung wenn jemand einen ihrer Beiträge geliked hat",
            'hasLikedComment': "Benachrichtigung wenn jemand eins ihrer Kommentare geliked hat",
            'hasNewComment': "Benachrichtigung wenn jemand ein Kommentar unter einem ihrer Beiträge verfasst hat",
            'hasSharedPost': "Benachrichtigung wenn jemand einen ihrer Beiträge geteilt hat"
        }
        widgets = {
            "hasAssetAmountChanged": forms.Select(choices=CHOICES),
            "hasNewFollower": forms.Select(choices=CHOICES),
            "hasLikedPost": forms.Select(choices=CHOICES),
            "hasLikedComment": forms.Select(choices=CHOICES),
            "hasNewComment": forms.Select(choices=CHOICES),
            "hasSharedPost": forms.Select(choices=CHOICES)
        }
