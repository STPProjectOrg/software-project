from django.http import JsonResponse
from django.shortcuts import render
from user_app.models import CustomUser
from core.templatetags.core_tags import search_result
from django.template.loader import render_to_string

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

def legal_disclosure(request):
    return render(request, 'core/legal_disclosure.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def cookie_disclosure(request):
    return render(request, 'core/cookie_disclosure.html')

def search_results(request):
    username = request.GET.get('username','')

    # Search for users with a similar username
    results = CustomUser.objects.filter(username__icontains=username)
    
    # result_list = [user for user in results]
    # return JsonResponse({'results': result_list})
    
    # result_list = [user.username for user in results]
    # return JsonResponse({'results': result_list})

    # result_list = [search_result(user.username) for user in results]
    result_list = [render_to_string('inclusion/search_result.html', {'username': user.username}) for user in results]
    return JsonResponse({'results': result_list})
