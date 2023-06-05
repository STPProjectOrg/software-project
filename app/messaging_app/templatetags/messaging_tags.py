""" Custom Tags for the core_app """

from datetime import datetime
from django import template


register = template.Library()

@register.inclusion_tag("messaging_app/modals/full_image_modal.html")
def full_image_modal(message):
    """ Include a modal for post creation. """

    return {"message":message}

