""" Custom Tags for the core_app """

from datetime import datetime
from django import template


register = template.Library()


@register.inclusion_tag("community_app/inclusion/post.html")
def entry(user, post):
    """ Include a post element. """

    return {"user": user, "post": post}


@register.inclusion_tag("community_app/modals/post_create_modal.html")
def post_create_modal(user, form):
    """ Include a modal for post creation. """

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
