""" Views for the core_app """

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from user_app.models import CustomUser
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
    username = request.GET.get('username', '')

    # Search for users with a similar username
    results = CustomUser.objects.filter(username__icontains=username)
    # result_string = render_to_string('inclusion/search_result.html', {'results': results})

    result_list = []
    for result in results:
        curren_user = get_object_or_404(CustomUser, username=result.username)
        username = curren_user.username
        pic = curren_user.userprofileinfo.profile_pic.url if curren_user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        icon = "bi bi-person-fill-check" if request.user.following.all().filter(
            following_user=curren_user).exists() else "bi bi-person-plus"
        result_list.append(render_to_string('inclusion/search_result.html', {'username': username,
                                                                             'pic': pic,
                                                                             'icon': icon}))

    return JsonResponse({'results': result_list})
