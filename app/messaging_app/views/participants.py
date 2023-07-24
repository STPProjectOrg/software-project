from messaging_app.models import InboxParticipants, Message, Inbox
from datetime import datetime
from ..utils import define_created_at


def get_participants(user):
    """
    Get a list of all participants of an inbox from the given user.

    Keyword arguments:
        user:               The user that is signed in.
        inbox_participants: The inbox participants.
    """

    inbox_from_user = Inbox.objects.get_or_create(inbox_from_user=user)
    participants = []
    for participant in InboxParticipants.objects.filter(inbox_id=inbox_from_user[0]):
        participants.append(
            {"participant": participant.participant_id, 
             "last_message": participant.last_message, 
             "last_message_sent_at": define_created_at(participant.last_message_sent_at),
             "unread_messages": Message.objects.filter(from_user=participant.participant_id, to_user=user).filter(message_read=False).__len__(),
             "participant_pic": user.userprofileinfo.profile_pic.url 
                                if user.userprofileinfo.profile_pic 
                                else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
            })
        
    return participants

def create_or_update_inbox_participant(user, chat_participant, message):
    """
    Create or update an 'InboxParticipant'-Entry after sending a message.

    Keyword arguments:
        user:               The user that sends the message.
        chat_participant:   The chat participant.
        message:            The last 'Message' that should get displayed.
    """
    
    inbox_user = Inbox.objects.get_or_create(inbox_from_user=user)
    last_message = message[0:20] + "..." if message.__len__() > 20 else message

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