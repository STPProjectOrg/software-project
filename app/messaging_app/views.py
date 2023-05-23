from django.shortcuts import render
from messaging_app.models import Inbox, InboxParticipants, Message
from user_app.models import CustomUser
from messaging_app.forms import AddParticipantForm, AddMessageForm
from datetime import datetime

# Create your views here.
def inbox(request):
    user = CustomUser.objects.get(id=request.user.id)
    inbox_from_user = Inbox.objects.get(inbox_from_user=user)
    inbox_participants = InboxParticipants.objects.filter(inbox_id=inbox_from_user.id)

    form = AddParticipantForm()
    if request.method=='POST':
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            participant_to_add = CustomUser.objects.get(id=d.get("participant"))
            InboxParticipants.objects.get_or_create(
                inbox_id = inbox_from_user,
                participant_id = participant_to_add
            )
    participants = []
    for participant in inbox_participants:
        participant_user = CustomUser.objects.get(id=participant.id)
        participant_pic = participant_user.userprofileinfo.profile_pic.url if participant_user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        participants.append({"participant": participant_user, "participant_pic":participant_pic})
    data = {"participants": participants, "form": form}
    return render(request, "messaging_app/inbox.html", context=data)

def chat(request, participant):
    user = CustomUser.objects.get(id=request.user.id)
    chat_participant = CustomUser.objects.get(username=participant)
    chat_messages_logged_in = Message.objects.filter(from_user=user, to_user=chat_participant)
    chat_messages_participant = Message.objects.filter(from_user=chat_participant, to_user=user)
    chat_messages = (chat_messages_logged_in | chat_messages_participant).order_by('created_at').values()

    form = AddMessageForm()
    if request.method=='POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
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

    data = {"user": user,"participant": chat_participant, "messages": messages, "form": form}
    return render(request, "messaging_app/chat.html", context=data)