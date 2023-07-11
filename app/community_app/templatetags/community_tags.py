""" Custom Tags for the core_app """

from datetime import datetime
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe
from user_app.models import CustomUser
from api_app.models import Asset
from community_app.views import post

register = template.Library()


@register.inclusion_tag("community_app/inclusion/post.html")
def entry(user, post):
    """ Include a post element. """

    return {"user": user, "post": post}


@register.inclusion_tag("community_app/modals/post_create_modal.html")
def post_create_modal(user):
    """ Include a modal for post creation. """

    form = post.PostForm()

    return {"user": user, "form": form}


@register.filter(name="to_tag_list")
def to_tag_list(string):
    """ Converts a string of tags seperated by ',' into a list of strings. """

    trimmed_string = string.replace(" ", "")
    return trimmed_string.split(",")


@register.filter(name="datetime_converter")
def datetime_converter(entry_datetime: datetime):
    """ Converts a datetime depending on the time since creation. """

    now = datetime.now()

    if entry_datetime.date() == now.date():
        return f"Heute {entry_datetime.hour}:{entry_datetime.minute}"

    if (now.date() - entry_datetime.date()).days == 1:
        return "Gestern"

    return f"{entry_datetime.day}.{entry_datetime.month}.{entry_datetime.year}"


@register.inclusion_tag("community_app/modals/full_image_modal.html")
def full_image_modal(post):
    """ Include a modal for post creation. """

    return {"post": post}


@register.filter
@stringfilter
def tag(value: str):
    if "@" in value:
        cut = value.split(" ")
        for current in cut:
            if current[0] == "@":
                if CustomUser.objects.filter(username=current[1:current.__len__()]).exists():
                    value = value.replace(
                        current, f'<a href="http://localhost:8000/auth/profile/{current[1:current.__len__()]}/">{current}</a>')
                elif Asset.objects.filter(name=current[1:current.__len__()].upper()).exists():
                    value = value.replace(
                        current, f'<a href="http://localhost:8000/dashboard_app/asset/{current[1:current.__len__()].lower()}">{current}</a>')

    return mark_safe(value)
