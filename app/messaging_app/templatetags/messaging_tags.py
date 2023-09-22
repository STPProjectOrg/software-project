""" Custom Tags for the messaging_app """

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe
from user_app.models import CustomUser
from api_app.models import Asset
from datetime import datetime, date

register = template.Library()


@register.inclusion_tag("messaging_app/modals/full_image_modal.html")
def full_image_modal(message):
    """ Include a modal for post creation. """

    return {"message": message}


@register.filter
@stringfilter
def tag(value: str):
    if "@" in value:
        cut = value.split(" ")
        for current in cut:
            if current[0] == "@":
                if CustomUser.objects.filter(username=current[1:current.__len__()]).exists():
                    value = value.replace(
                        current, f'<a href="http://localhost:8000/auth/profile/{current[1:current.__len__()]}/0/">{current}</a>')
                elif Asset.objects.filter(name=current[1:current.__len__()].upper()).exists():
                    value = value.replace(
                        current, f'<a href="http://localhost:8000/dashboard/asset/{current[1:current.__len__()]}/0">{current}</a>')

    return mark_safe(value)


@register.filter
def format_date(datetime: datetime):
    if datetime != None:
        created_at = datetime
        if created_at.date() == date.today():
            created_at = str(datetime.hour) + ":" + \
                str("%02d" % (datetime.minute,))
        elif (date.today() - created_at.date()).days >= 2:
            created_at = str("%02d" % (datetime.day,)) + "." + \
                str("%02d" % (datetime.month,)) + "." + str(datetime.year)
        elif (date.today() - created_at.date()).days >= 1:
            created_at = "Gestern"
        return created_at
