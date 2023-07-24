from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .participants import get_participants

@login_required
def inbox(request):
    ''' Render the Inbox page with chat closed '''

    participants = get_participants(request.user)

    data = {"chatOpen": False,
            "participants": participants}

    return render(request, "messaging_app/inbox.html", context=data)

