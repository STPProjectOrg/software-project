from django.shortcuts import render

def debug(request):
    """ Renders a custom url for debug purposes """
    url = 'core/base.html'
    return render(request, url)

def index(request):
    """
    TODO: Check if user is logged in
    if (logged in)
        return private area
    else
        return landing page
    """

    return landing_page(request)

def landing_page(request):
    return render(request, 'core/landing.html')

def register(request):
    return render(request, '')

def signin(request):
    return render(request, '')

