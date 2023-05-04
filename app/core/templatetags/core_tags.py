from django import template

register = template.Library()


@register.inclusion_tag("inclusion/logo_name.html")
def logo_name():
    return


@register.inclusion_tag("inclusion/navigation.html")
def navigation():
    return


@register.inclusion_tag("inclusion/footer.html")
def footer():
    return
