
from django.http import JsonResponse
from django.template.loader import render_to_string
from api_app.models import Asset
from user_app.models import CustomUser
from django.db.models import Q


def results(request):
    # Get the search value from the request
    search_value = request.GET.get('input', '')

    # Search for users and assets with a similar search value
    user_results = CustomUser.objects.filter(Q(username__icontains=search_value) | Q(
        first_name__icontains=search_value) | Q(last_name__icontains=search_value))[:5]
    asset_results = Asset.objects.filter(
        Q(name__icontains=search_value) | Q(coinName__icontains=search_value))[:5]

    # Get the following-list by the signed user
    user_following_list = request.user.following.values_list(
        "following_user_id", flat=True)

    # Create the result dictionary with the corresponding lists and hand them over to the template 'search_result.html'
    results = {'users': user_results, 'assets': asset_results,
               'followers': user_following_list}
    response = [render_to_string('inclusion/search_result.html', results)]

    return JsonResponse({'results': response})
