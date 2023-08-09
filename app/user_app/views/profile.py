""" Functions related to the user profile. """
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from settings_app.models import Settings
from dashboard_app.views import charts
from user_app.models import CustomUser, UserFollowing
from api_app.models import Asset
from dashboard_app.models import Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from dashboard_app.views import kpi
from community_app.views import post

@login_required
def profile_redirect(request):
    """ 
    Gets the username from the request parameter to build the redirect url to
    the profile page

    Keyword arguments:
        request: The http request
    """
    username = request.user.username
    profile_url = reverse('user_app:profile', kwargs={'username': username, 'timespan': 0})
    return redirect(profile_url)


@login_required
def profile(request, username, timespan):
    """ 
    Render a user-profile.

    Keyword arguments:
        request: The http request
        username (str): The profile user's username
        timespan (int): The time span for the portfolio line chart data.
    """
    # Get profile user
    profile_user = get_object_or_404(
        CustomUser.objects.select_related("userprofileinfo"), username=username)

    # Declare common variables
    is_user_profile = request.user.username == profile_user.username
    portfolio_privacy_setting = Settings.objects.get_or_create(user=profile_user)[0].dashboard_privacy_settings

    # Get profile user's follow-lists
    profile_followers_list = CustomUser.objects.filter(
        following__following_user_id=profile_user.id).select_related("userprofileinfo")
    profile_following_list = CustomUser.objects.filter(
        followers__follower_user_id=profile_user.id).select_related("userprofileinfo")
    
    # Get follower list of the signed user 
    user_following_list = request.user.following.values_list(
        "following_user_id", flat=True)
    is_user_following = profile_user.userprofileinfo.id in user_following_list 

    # Post-Section
    my_posts = post.get_by_user(profile_user)
    postform = post.PostForm()

    # Chart Data
    chart_data = get_chart_data(profile_user.id, portfolio_privacy_setting, timespan)

    return render(request, 'user_app/profile.html',
                  {"profile_user": profile_user,
                   'user_profile_id': profile_user.userprofileinfo.id,
                   "is_user_profile": is_user_profile,
                   "is_user_following": is_user_following,
                   "portfolio_privacy_setting": portfolio_privacy_setting,
                   "profile_followers_list": profile_followers_list,
                   "profile_following_list": profile_following_list,
                   "user_following_list": user_following_list,
                   "postform": postform,
                   "myposts": my_posts,
                   "pie_data": chart_data["pie_data"],
                    "line_data": chart_data["line_data"],
                    "assets": chart_data["assets"],
                    "kpi_total": chart_data["kpi_total"],
                    "has_transactions": chart_data["has_transactions"],
                   })


def get_chart_data(user_id, privacy_setting, timespan):
    """
    Get chart data for a user's portfolio.

    Parameters:
        user_id (int): The ID of the user.
        privacy_setting (str): The privacy setting for displaying asset values.
        timespan (int): The time span for the portfolio line chart data.

    Returns:
        dict: A dictionary containing the following chart data:
              - "assets": QuerySet of assets associated with the user's transactions.
              - "pie_data": Data for a pie chart.
              - "line_data": Data for a portfolio line chart over the specified timespan.
              - "has_transactions": A boolean indicating whether the user has any transactions.
              - "kpi_total": The total Key Performance Indicator (KPI) for the user's portfolio.
              - "anonymize": A boolean indicating whether asset values should be anonymized based
                              on the privacy setting.
    """
    transactions = Transaction.objects.filter(user=user_id)
    
    assets = Asset.objects.filter(transaction__user=user_id).annotate(
        amount=Sum("transaction__amount"),
        cost=Sum("transaction__cost"),
        total_value=F("amount") * F("price"),
        profit=F("total_value") - F("cost")
    ).distinct()

    has_transactions = bool(transactions)
    kpi_total = kpi.get_kpi(transactions, assets)["total"] if has_transactions else 0
    anonymize = True if privacy_setting == "without values" else False    

    pie_data = charts.get_pie_data(assets, anonymize)
    line_data = charts.get_portfolio_line_data(transactions, timespan, anonymize)
    
    return {
        "assets": assets,
        "pie_data": pie_data,
        "line_data": line_data,
        "has_transactions": has_transactions,
        "kpi_total": kpi_total,
        "anonymize": anonymize,
    }


@login_required
def toggle_follow(request, username):
    """
    Toggle the follow status between the logged-in user and another user.
    It allows a logged-in user to follow or unfollow another user's profile.
    The follow status is toggled based on whether the logged-in user is already 
    following the other user.

    Keyword arguments:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user to follow or unfollow.
    """
    # Get the profile of the logged-in user and the profile of the other user
    profile_user = CustomUser.objects.get(username=request.user.username)
    other_user = get_object_or_404(CustomUser, username=username)

    # Check if the logged-in user is not the same as the other user
    if profile_user != other_user:
        # Check if the logged-in user is already following the other use
        if profile_user.following.all().filter(following_user=other_user).exists():
            # Unfollow the other user by deleting the UserFollowing relationship
            UserFollowing.objects.filter(
                follower_user=profile_user, following_user=other_user).delete()
        else:
            # Follow the other user by creating a new UserFollowing relationship
            UserFollowing.objects.create(
                follower_user=profile_user, following_user=other_user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

