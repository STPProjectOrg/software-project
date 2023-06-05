""" Custom Tags for the messaging_app """

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe
from user_app.models import CustomUser
from api_app.models import Asset

register = template.Library()

@register.inclusion_tag("messaging_app/modals/full_image_modal.html")
def full_image_modal(message):
    """ Include a modal for post creation. """

    return {"message":message}

@register.filter
@stringfilter
def tag(value : str):
    if "@" in value:
        cut = value.split(" ")
        for current in cut:
            if current[0] == "@":
                if CustomUser.objects.filter(username=current[1:current.__len__()]).exists():
                    value = value.replace(current, f'<a href="http://localhost:8000/auth/profile/{current[1:current.__len__()]}/">{current}</a>')
                elif Asset.objects.filter(name=current[1:current.__len__()].upper()).exists():
                    value = value.replace(current, f'<a href="http://localhost:8000/dashboard_app/asset/{current[1:current.__len__()].lower()}">{current}</a>')

    return mark_safe(value)
