from messaging_app.models import Message
from django.http import HttpResponseRedirect
from messaging_app.forms import AddMessageForm
from user_app.models import CustomUser
from datetime import datetime
from .participants import create_or_update_inbox_participant

def create_message(request, chat_participant_name):
    """
    Create a 'Message'.

    Keyword arguments:
        chat_participant_name: The name of the chat participant.
    """

    chat_participant = CustomUser.objects.get(username=chat_participant_name)
    form = AddMessageForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.cleaned_data
        Message.objects.create(
            from_user = request.user,
            to_user = chat_participant,
            message = data["message"],
            message_read = False,
            created_at = datetime.now(),
            image = data["image"]
        )

    create_or_update_inbox_participant(request.user, chat_participant, data["message"])
    create_or_update_inbox_participant(chat_participant, request.user, data["message"])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_chat_messages(user, chat_participant):
    """
    Get a list of all chat 'Messages' between the user and the chat participant.

    Keyword arguments:
        user:               The user that is signed in.
        chat_participant:   The chat participant.
    """
        
    chat_messages_user_logged_in = Message.objects.filter(
        from_user=user, to_user=chat_participant)
    
    chat_messages_participant = Message.objects.filter(
        from_user=chat_participant, to_user=user)
    
    chat_messages_combined = (chat_messages_user_logged_in |
                     chat_messages_participant).order_by('created_at')
    
    update_message_read(chat_messages_combined, chat_participant)

    return reversed(chat_messages_combined)

def update_message_read(messages, chat_participant):
    """
    Update all 'Message' and set 'message_read = True'.

    Keyword arguments:
        messages:           All messages between the users.
        chat_participant:   The chat participant.
    """
        
    for mes in messages:
        if mes.message_read == False:
            Message.objects.filter(id=mes.id, from_user=chat_participant).update(message_read = True)