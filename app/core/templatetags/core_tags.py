""" Custom Tags for the core_app """

from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("inclusion/search_modal.html")
def search_modal():
    return


@register.inclusion_tag("inclusion/search_result.html")
def search_result(username):
    return {'username': username}


@register.inclusion_tag("inclusion/logo_name.html")
def logo_name():
    """ Include the logo and name element. """

    return


@register.inclusion_tag("inclusion/logo.html")
def logo():
    """ Include the logo element. """

    return


@register.inclusion_tag("inclusion/user_menu.html")
def user_menu(request):
    """ Include the user menu element. """

    return {'request': request}


@register.inclusion_tag("inclusion/navigation.html")
def navigation():
    """ Include the navigation element. """

    return


@register.inclusion_tag("inclusion/navigation_button.html")
def navigation_button(name, icon, route, *args, **kwargs):
    """
    Include a navigation button.

    Keyword arguments:
        name: The name to be displayed.
        icon: The icon to be displayed (bootstrap icon class).
        route: The reversed url of the given page ('app:route' args).
        *args, **kwargs: Additional route parameter.
    """

    # Resolve route
    resolved_route = reverse(route, None, args, kwargs)

    return {'name': name,
            'route': resolved_route,
            'icon': icon}


@register.inclusion_tag("inclusion/footer.html")
def footer():
    """ Include the footer element. """

    return


@register.inclusion_tag("inclusion/search.html")
def search(width):
    return {'width': width}
