""" Functions related to the user authentification. """

from django.contrib.auth import logout as django_logout
from django.shortcuts import render


def logout(request):
    """ Logout the current user and redirect to home view. """

    django_logout(request)
    return render(request, "core:landing")
