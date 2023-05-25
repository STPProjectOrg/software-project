from django.shortcuts import render
from messaging_app.models import Inbox, InboxParticipants, Message
from user_app.models import CustomUser
from messaging_app.forms import AddMessageForm
from datetime import datetime

# Create your views here.
def inbox(request):
    user = CustomUser.objects.get(id=request.user.id)
    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=user)
    participants = get_participants(InboxParticipants.objects.filter(inbox_id=inbox_from_user[0]))

    data = {"chatOpen": False,"participants": participants, "participant": "", "messages": "", "form": ""}

    return render(request, "messaging_app/inbox.html", context=data)

def inbox_chat(request, participant_req):
    user = CustomUser.objects.get(id=request.user.id)
    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=user)
    participants = get_participants(InboxParticipants.objects.filter(inbox_id=inbox_from_user[0]))

    # Chat
    chat_participant = CustomUser.objects.get(username=participant_req)
    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=user)
    InboxParticipants.objects.get_or_create(
                inbox_id = inbox_from_user[0],
                participant_id = chat_participant
            )
    chat_messages_user_logged_in = Message.objects.filter(from_user=user, to_user=chat_participant)
    chat_messages_participant = Message.objects.filter(from_user=chat_participant, to_user=user)
    chat_messages = (chat_messages_user_logged_in | chat_messages_participant).order_by('created_at').values()

    form = AddMessageForm()
    if request.method=='POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            inbox_participant = Inbox.objects.get_or_create(inbox_from_user=chat_participant)
            InboxParticipants.objects.get_or_create(
                inbox_id = inbox_participant[0],
                participant_id = user
            )
            message = d.get("message")
            Message.objects.create(
                from_user = user,
                to_user = chat_participant,
                message = message,
                created_at = datetime.now()
            )
    messages = []
    for mes in chat_messages:
        messages.append(mes)

    data = {"chatOpen": True, "user": user,"participants": participants, "participant": chat_participant, "messages": messages, "form": form}
    return render(request, "messaging_app/inbox.html", context=data)

def get_participants(inbox_participants):
    participants = []
    for participant in inbox_participants:
        participant_user = CustomUser.objects.get(username=participant.participant_id)
        participant_pic = participant_user.userprofileinfo.profile_pic.url if participant_user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        participants.append({"participant": participant_user, "participant_pic":participant_pic})
    return participants