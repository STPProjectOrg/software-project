from django.shortcuts import get_object_or_404, render
from settings_app.models import Settings
from dashboard_app.views import charts
from user_app.models import CustomUser
from api_app.models import Asset
from dashboard_app.models import Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from dashboard_app.views import kpi
from community_app.views import post

@login_required
def profile(request, username, timespan):
    """ 
    Render a user-profile.

    Keyword arguments:
        request: The http request
        username: The profile user's username
    """

    # Get profile user
    profile_user = get_object_or_404(
        CustomUser.objects.select_related("userprofileinfo"), username=username)

    # Declare common variables
    user_following_list = request.user.following.values_list(
        "following_user_id", flat=True)
    is_user_profile = request.user.username == profile_user.username
    is_user_following = profile_user.userprofileinfo.id in user_following_list

    portfolio_privacy_setting = Settings.objects.get_or_create(user=profile_user)[0].dashboard_privacy_settings


    # Get profile user's follow-lists
    profile_followers_list = CustomUser.objects.filter(
        following__following_user_id=profile_user.id).select_related("userprofileinfo")
    profile_following_list = CustomUser.objects.filter(
        followers__follower_user_id=profile_user.id).select_related("userprofileinfo")

    # Post-Section
    my_posts = post.get_by_user(profile_user)
    postform = post.PostForm()

    # Chart Data

    transactions = Transaction.objects.filter(user=profile_user.id)
    assets = Asset.objects.filter(transaction__user=profile_user.id).annotate(
        amount=Sum("transaction__amount"),
        cost=Sum("transaction__cost"),
        total_value=F("amount") * F("price"),
        profit=F("total_value") - F("cost")
    ).distinct()

    if not assets:
        data = {"assets": None}

    has_transactions = False
    kpi_total = 0
    
    if transactions:
        kpi_total = kpi.get_kpi(transactions, assets)["total"]
        has_transactions = True

    if portfolio_privacy_setting == "without values":
        kpi_total = 0
        anonymize = True
    else:
        anonymize = False

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
                   "pie_data": charts.get_pie_data(assets, anonymize),
                    "line_data": charts.get_portfolio_line_data(transactions, timespan, anonymize),
                    "assets": assets,
                    "kpi_total": kpi_total,
                    "has_transactions":has_transactions,
                   })