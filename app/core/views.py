from django.shortcuts import render
from user_app import views as user_views


def debug(request):
    """ Renders a custom url for debug purposes """
    url = 'core/base.html'
    return render(request, url)


def index(request):

    if request.user.is_authenticated:
        return user_views.profile(request, request.user.username)
    else:
        return render(request, 'core/landing.html')


def landing_page(request):
    return render(request, 'core/landing.html')


def register(request):
    return render(request, '')


def signin(request):
    return render(request, '')


def legal_disclosure(request):
    return render(request, 'core/legal_disclosure.html')


def privacy(request):
    return render(request, 'core/privacy.html')


def cookie_disclosure(request):
    return render(request, 'core/cookie_disclosure.html')
