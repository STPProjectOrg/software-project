from django.shortcuts import render
from messaging_app.models import Inbox, InboxParticipants, Message
from user_app.models import CustomUser
from messaging_app.forms import AddMessageForm
from datetime import datetime, date, timezone
from messaging_app.utils import compress_image
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def inbox(request):
    user = request.user
    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=user)
    participants = get_participants(user, 
        InboxParticipants.objects.filter(inbox_id=inbox_from_user[0]))

    data = {"chatOpen": False, "participants": participants,
            "participant": "", "messages": "", "form": ""}

    return render(request, "messaging_app/inbox.html", context=data)

@login_required
def inbox_chat(request, participant_req):
    user = request.user
    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=user)
    participants = get_participants(user=user, inbox_participants=InboxParticipants.objects.filter(inbox_id=inbox_from_user[0]))
    chat_participant = CustomUser.objects.select_related("userprofileinfo").get(username=participant_req)
    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=user)
    InboxParticipants.objects.get_or_create(
        inbox_id=inbox_from_user[0],
        participant_id=chat_participant
    )
    # Chat
    form = AddMessageForm()
    if request.method == 'POST':
        form = AddMessageForm(request.POST, request.FILES)
        if form.is_valid():
            d = form.cleaned_data
            message = d.get("message")
            update_inbox_participant(user, chat_participant, message)
            update_inbox_participant(chat_participant, user, message)

            Message.objects.create(
                from_user=user,
                to_user=chat_participant,
                message=message,
                message_read = False,
                created_at=datetime.now(),
                image = compress_image(d.get("image"))
            )
            form = AddMessageForm()
    messages = []
    for mes in get_chat_messages(user, chat_participant):
        if mes.message_read == False:
            Message.objects.filter(id=mes.id, from_user=chat_participant).update(message_read = True)
        messages.insert(0, mes)

    data = {"chatOpen": True, "user": user, "participants": participants,
            "participant": chat_participant, "messages": messages, "form": form}
    return render(request, "messaging_app/inbox.html", context=data)



def get_participants(user, inbox_participants):
    participants = []
    for participant in inbox_participants:
        participant_user = CustomUser.objects.get(
            username=participant.participant_id)
        participant_pic = participant_user.userprofileinfo.profile_pic.url if participant_user.userprofileinfo.profile_pic else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
        last_message_sent_at = define_created_at(participant.last_message_sent_at)
        participants.append(
            {"participant": participant_user, 
             "last_message": participant.last_message, 
             "last_message_sent_at": last_message_sent_at,
             "unread_messages": Message.objects.filter(from_user=participant_user, to_user=user).filter(message_read=False).__len__(),
             "participant_pic": participant_pic})
    return participants

def get_chat_messages(user, chat_participant):
    chat_messages_user_logged_in = Message.objects.filter(
        from_user=user, to_user=chat_participant)
    chat_messages_participant = Message.objects.filter(
        from_user=chat_participant, to_user=user)
    chat_messages = (chat_messages_user_logged_in |
                     chat_messages_participant).order_by('created_at')
    return chat_messages

def update_inbox_participant(user, chat_participant, message):
            inbox_user = Inbox.objects.get_or_create(inbox_from_user=user)
            if message.__len__() > 20:
                last_message = message[0:20] + "..."
            else:
                 last_message = message
            if InboxParticipants.objects.filter(inbox_id=inbox_user[0],participant_id=chat_participant).exists():
                InboxParticipants.objects.filter(inbox_id=inbox_user[0],participant_id=chat_participant).update(
                    inbox_id=inbox_user[0],
                    participant_id=chat_participant,
                    last_message = last_message,
                    last_message_sent_at = datetime.now()
                )
            else:
                InboxParticipants.objects.create(
                    inbox_id=inbox_user[0],
                    participant_id=chat_participant,
                    last_message = last_message,
                    last_message_sent_at = datetime.now()
                )

def define_created_at(datetime: datetime):
        if datetime != None:
            created_at = datetime
            if created_at.date() == datetime.today():
                created_at = datetime
            elif (date.today() - created_at.date()).days >= 2 :
                created_at = datetime.date()
            elif (date.today() - created_at.date()).days >= 1 :
                created_at = "Gestern"
            return created_at