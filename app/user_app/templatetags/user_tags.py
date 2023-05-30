from django import template

register = template.Library()

# inclusion_tags


@register.inclusion_tag("modals/profile_image_modal.html")
def profile_image_modal(user_id):
    return {"user_id": user_id}


@register.inclusion_tag("modals/profile_banner_modal.html")
def profile_banner_modal():
    return


@register.inclusion_tag("modals/profile_following_modal.html")
def profile_following_modal(request, profile_user, profile_following_list, user_following_list):
    return {"request": request, "profile_user": profile_user, "profile_following_list": profile_following_list, "user_following_list": user_following_list}


@register.inclusion_tag("modals/profile_followers_modal.html")
def profile_followers_modal(request, profile_user, profile_followers_list, user_following_list):
    return {"request": request, "profile_user": profile_user, "profile_followers_list": profile_followers_list, "user_following_list": user_following_list}
