""" Custom Tags for the core_app """

from datetime import datetime
from django import template
from django.urls import reverse
from api_app.models import Asset

from api_app.views import getCryptoValueFromDatabase, getCoinInformation
import cryptocompare

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
def navigation(username):
    """ Include the navigation element. """

    return {'username': username}


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


@register.filter
def get_asset_value(asset: Asset):
    """ Returns the price of a given asset in EUR. """

    value = cryptocompare.get_price(asset.name, currency='EUR')[
        asset.name]['EUR']

    return to_locale_valuta(value)


@register.filter
def to_locale_valuta(value):
    # Add thousands separators and format to 2 decimal places
    formatted_value = f'{value:,.2f}'
    # Replace the decimal separator with a comma
    formatted_value = formatted_value.replace(',', '#')
    formatted_value = formatted_value.replace('.', ',')
    formatted_value = formatted_value.replace('#', '.')
    return formatted_value + " €"


@register.filter
def get_asset_picture(asset):
    return getCoinInformation(asset.name).get("ImageUrl")
