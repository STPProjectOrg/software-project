""" Custom Tags for the "Core Application" """

from django import template

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
def navigation_button(name, route, icon):
    return {'name': name,
            'route': route,
            'icon': icon}


@register.inclusion_tag("inclusion/footer.html")
def footer():
    return


@register.inclusion_tag("inclusion/search.html")
def search(width):
    return {'width': width}
