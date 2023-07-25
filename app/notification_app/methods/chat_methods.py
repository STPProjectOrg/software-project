
from datetime import datetime
from channels.db import database_sync_to_async


from messaging_app.models import Inbox, InboxParticipants, Message
from messaging_app.utils import define_created_at
from user_app.models import CustomUser


@database_sync_to_async
def save_channel_layer(user_pk, channel_layer):
    """
    Save the channel layer.

    Keyword arguments:
        channel_layer: The channel layer.
    """
    user = CustomUser.objects.get(id=user_pk)
    user.channel_name = channel_layer
    user.save()


@database_sync_to_async
def remove_channel_layer(user_pk):
    """
    Remove the channel layer.

    Keyword arguments:
        user_pk: The primary key of the user.
    """
    user = CustomUser.objects.get(id=user_pk)
    user.channel_name = ""
    user.save()


@database_sync_to_async
def create_message(from_user, to_user_username, message, image):
    """
    Create a 'Message'.

    Keyword arguments:
        chat_participant_name: The name of the chat participant.
    """

    to_user = CustomUser.objects.get(username=to_user_username)
    data = Message.objects.create(
        from_user=from_user,
        to_user=to_user,
        message=message,
        message_read=False,
        created_at=datetime.now(),
        image=image
    )

    create_or_update_inbox_participant(
        from_user, to_user, message)
    create_or_update_inbox_participant(
        to_user, from_user, message)

    return data


@database_sync_to_async
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
            {"participant": participant.participant_id.pk,
             "last_message": participant.last_message,
             "last_message_sent_at": f"{define_created_at(participant.last_message_sent_at)}",
             "unread_messages": Message.objects.filter(from_user=participant.participant_id, to_user=user).filter(message_read=False).__len__(),
             "participant_pic": user.userprofileinfo.profile_pic.url
             if user.userprofileinfo.profile_pic
             else "http://ssl.gstatic.com/accounts/ui/avatar_2x.png"
             })

    return participants


@database_sync_to_async
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

    if InboxParticipants.objects.filter(inbox_id=inbox_user[0], participant_id=chat_participant).exists():
        InboxParticipants.objects.filter(inbox_id=inbox_user[0], participant_id=chat_participant).update(
            inbox_id=inbox_user[0],
            participant_id=chat_participant,
            last_message=last_message,
            last_message_sent_at=datetime.now()
        )
    else:
        InboxParticipants.objects.create(
            inbox_id=inbox_user[0],
            participant_id=chat_participant,
            last_message=last_message,
            last_message_sent_at=datetime.now()
        )
