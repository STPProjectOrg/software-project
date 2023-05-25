""" Custom Tags for the "Core Application" """

from django import template
from django.urls import reverse

register = template.Library()

# inclusion_tags


@register.inclusion_tag("inclusion/search_modal.html")
def search_modal():
    return


@register.inclusion_tag("inclusion/search_result.html")
def search_result(username):
    return {'username': username}


@register.inclusion_tag("inclusion/logo_name.html")
def logo_name():
    return


@register.inclusion_tag("inclusion/logo.html")
def logo():
    return


@register.inclusion_tag("inclusion/user_menu.html")
def user_menu(request):
    return {'request': request}


@register.inclusion_tag("inclusion/navigation.html")
def navigation():
    return


@register.inclusion_tag("inclusion/navigation_button.html")
def navigation_button(name, icon, route, *args, **kwargs):
    """
    Include a navigation button.

    Keyword arguments:
        name: The name to be displayed.
        icon: The icon to be displayed.
        route: The url of the given page.
        args, kwargs: Additional route parameter.
    """

    resolved_route = reverse(route, None, args, kwargs)

    return {'name': name,
            'route': resolved_route,
            'icon': icon}


@register.inclusion_tag("inclusion/footer.html")
def footer():
    return


@register.inclusion_tag("inclusion/search.html")
def search(width):
    return {'width': width}
