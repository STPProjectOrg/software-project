""" Custom Tags for the core_app """

from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("community_app/inclusion/post.html")
def entry(user, post):
    """ Include a post element. """

    return {"user": user, "post": post}
