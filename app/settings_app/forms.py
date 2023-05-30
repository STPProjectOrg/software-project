from django import forms
from .models import Settings

# TODO: Template String für Internationalisierung der Dropdown Texte
CHOICES = [(False, 'Deaktiviert'), (True, 'Aktiviert')]


class notificationSettingsForm(forms.Form):

    hasAssetAmountChanged = forms.BooleanField(
        label="Benachrichtigung bei Veränderung der Assetmenge", required=False, widget=forms.Select(choices=CHOICES))
    hasNewFollower = forms.BooleanField(
        label="Benachrichtigung wenn ihnen jemand folgt", required=False, widget=forms.Select(choices=CHOICES))
    hasLikedPost = forms.BooleanField(
        label="Benachrichtigung wenn jemand einen ihrer Beiträge geliked hat", required=False, widget=forms.Select(choices=CHOICES))
    hasLikedComment = forms.BooleanField(
        label="Benachrichtigung wenn jemand eins ihrer Kommentare geliked hat", required=False, widget=forms.Select(choices=CHOICES))
    hasNewComment = forms.BooleanField(
        label="Benachrichtigung wenn jemand ein Kommentar unter einem ihrer Beiträge verfasst hat", required=False, widget=forms.Select(choices=CHOICES))
    hasSharedPost = forms.BooleanField(
        label="Benachrichtigung wenn jemand einen ihrer Beiträge geteilt hat", required=False, widget=forms.Select(choices=CHOICES))
