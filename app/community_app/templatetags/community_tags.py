""" Custom Tags for the core_app """

from django import template
from django.urls import reverse

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
    trimmed_string = string.replace(" ", "")
    return trimmed_string.split(",")
