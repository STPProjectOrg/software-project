from django import template

register = template.Library()


@register.inclusion_tag("inclusion/logo_name.html")
def logo_name():
    return
