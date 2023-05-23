from django import template

register = template.Library()

# inclusion_tags
@register.inclusion_tag("inclusion/search_result.html")
def search_result(username):
    return {'username': username}

@register.inclusion_tag("inclusion/logo_name.html")
def logo_name():
    return

@register.inclusion_tag("inclusion/logo.html")
def logo():
    return


@register.inclusion_tag("inclusion/navigation.html")
def navigation():
    return


@register.inclusion_tag("inclusion/footer.html")
def footer():
    return


@register.inclusion_tag("inclusion/search.html")
def search(width):
    return {'width': width}
