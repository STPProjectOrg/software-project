""" Views for the core_app """

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from api_app.models import Asset
from user_app.models import CustomUser
from django.db.models import Q
from user_app import views as user_views


def debug(request):
    """ Render a custom url for debug purposes. """

    url = 'core/base.html'
    return render(request, url)


def index(request):
    """ 
        Render either the landing page or a user's profile page 
        depending on a user's authentication status. 
    """

    if request.user.is_authenticated:
        return user_views.profile(request, request.user.username)

    return render(request, 'core/landing.html')


def landing_page(request):
    """ Render the landing page. """

    return render(request, 'core/landing.html')


def register(request):
    """ Render the registration page. """
    return render(request, '')


def signin(request):
    """ Render the login page. """

    return render(request, '')


def legal_disclosure(request):
    """ Render the legal disclosure page. """

    return render(request, 'core/legal_disclosure.html')


def privacy(request):
    """ Render the privacy disclosure page. """

    return render(request, 'core/privacy.html')


def cookie_disclosure(request):
    """ Render the cookie disclosure page. """

    return render(request, 'core/cookie_disclosure.html')


def question_and_answers(request):
    """ Render the questions and answers page. """

    return render(request, 'core/questions_and_answers.html')


def search_results(request):
    # Get the search value from the request
    search_value = request.GET.get('username', '')

    # Search for users and assets with a similar search value 
    user_results = CustomUser.objects.filter(username__icontains=search_value)
    asset_results = Asset.objects.filter(Q(name__icontains=search_value) | Q(coinName__icontains=search_value))

    # Get the following-list by the signed user 
    user_following_list = request.user.following.values_list(
        "following_user_id", flat=True)
    
    # Create the result dictionary with the corresponding lists and hand them over to the template 'search_result.html'
    results = {'users': user_results, 'assets': asset_results, 'followers': user_following_list}
    response = [render_to_string('inclusion/search_result.html', results)]

    return JsonResponse({'results': response})
