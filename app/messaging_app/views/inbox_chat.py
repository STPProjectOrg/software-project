from django.shortcuts import render
from messaging_app.models import Inbox, InboxParticipants
from user_app.models import CustomUser
from messaging_app.forms import AddMessageForm
from .participants import get_participants
from .messages import get_chat_messages
from django.contrib.auth.decorators import login_required

@login_required
def inbox_chat(request, participant_req):
    ''' Render the Inbox page with chat open '''

    chat_participant = CustomUser.objects.select_related("userprofileinfo").get(username=participant_req)
    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=request.user)
    InboxParticipants.objects.get_or_create(
        inbox_id=inbox_from_user[0],
        participant_id=chat_participant
    )

    data = {"chatOpen": True, 
            "user": request.user, 
            "participants": get_participants(request.user),
            "participant": chat_participant, 
            "messages": get_chat_messages(request.user, chat_participant), 
            "form": AddMessageForm()}
    
    return render(request, "messaging_app/inbox.html", context=data)

