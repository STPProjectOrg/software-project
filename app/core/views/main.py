""" Views for the core_app """

from django.shortcuts import render

from user_app.views import profile


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
        return profile.profile(request, request.user.username, 0)

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
