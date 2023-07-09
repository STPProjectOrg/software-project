from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from user_app.models import UserProfileInfo


@login_required
def update(request):
    """ Update a users biography. """

    if request.method == 'POST':
        information = UserProfileInfo.objects.get(id=request.user.id)

        information.biography = request.POST["biography"]
        information.save()

    return redirect(reverse('user_app:profile_redirect'))
