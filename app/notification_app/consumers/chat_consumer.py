import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from user_app.models import CustomUser

from notification_app.methods.chat_methods import create_message, create_or_update_inbox_participant, get_chat_messages, get_participants, remove_channel_layer, save_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    This class represents a ChatConsumer.
    """

    async def websocket_connect(self, message):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()
            await save_channel_layer(
                self.scope["user"].id, self.channel_layer)
            await self.send(
                json.dumps({
                    "type": "websocket.connect",
                    "consumer": "chat_consumer",
                    "message": "Successfully connected to chat_websocket."
                })
            )

            await self.channel_layer.send(
                self.channel_name,
                {
                    "type": "websocket.inbox_messages",
                    "consumer": "chat_consumer",
                }
            )

    async def websocket_receive(self, message):
        await self.send(
            json.dumps({
                "type": "websocket.receive",
                "consumer": "chat_consumer",
                "message": "Received message."
            })
        )

        await self.channel_layer.add(
            {
                "type": "websocket.create_message",
                "message": message
            }
        )

    async def websocket_disconnect(self, message):
        await remove_channel_layer(self.scope["user"].id)
        raise StopConsumer()

    async def websocket_create_message(self, message):
        """
        This method is used to create a 'Message'.
        """
        data = message.get("data")
        receiver = CustomUser.objects.get(id=data["to_user"]).channel_name

        message = await create_message(
            data["from_user"],
            data["to_user"],
            data["message"],
            data["image"]
        )

        await self.send(
            json.dumps({
                "type": "websocket.create_message",
                "consumer": "chat_consumer",
                "message": message,
            })
        )

        # Es müssen hierbei nachrichten an beide channel_layer gesendet werden
        # Empfänger und Sender
        self.channel_layer.send(
            {
                "type": "websocket.create_or_update_inbox_participant",
                "consumer": "chat_consumer",
                "data": {
                    "from_user": data["from_user"],
                    "to_user": data["to_user"],
                    "message": data["message"]
                }
            }
        )

    async def websocket_inbox_messages(self, message):
        """
        This method is used to send all messages of an inbox to the user.
        """

        participants = await get_participants(self.scope["user"])

        await self.send(
            json.dumps({
                "type": "websocket.inbox_messages",
                "consumer": "chat_consumer",
                "participants": participants,
            })
        )

    async def websocket_chat_messages(self, message):
        """
        This method is used to send all messages of a chat to the user.
        """
        messages = await get_chat_messages(
            self.scope["user"], message["chat_participant"])

        await self.send(
            json.dumps({
                "type": "websocket.chat_messages",
                "consumer": "chat_consumer",
                "messages": messages,
            })
        )

    async def websocket_chat_and_inbox_messages(self, message):
        """
        This method is used to send all messages of a chat and the inbox to the user.
        """
        participants = await get_participants(self.scope["user"])
        messages = await get_chat_messages(
            self.scope["user"], message["chat_participant"])

        await self.send(
            json.dumps({
                "type": "websocket.chat_and_inbox_messages",
                "consumer": "chat_consumer",
                "participants": participants,
                "messages": messages,
            })
        )

    async def websocket_create_or_update_inbox_participant(self, message):
        """
        This method is used to create or update an 'InboxParticipant'-Entry after sending a message.
        """
        data = message.get("data")
        receiver = CustomUser.objects.get(id=data["to_user"]).channel_name
        create_or_update_inbox_participant(
            data["from_user"],
            data["to_user"],
            data["message"]
        )
        create_or_update_inbox_participant(
            data["to_user"],
            data["from_user"],
            data["message"]
        )

        await self.send(
            json.dumps({
                "type": "websocket.create_or_update_inbox_participant",
                "consumer": "chat_consumer",
                "message": "Updated inbox of both users.",
            })
        )

        self.channel_layer.send(
            {
                "type": "websocket.chat_and_inbox_messages",
                "consumer": "chat_consumer",
            }
        )

        receiver.send(
            json.dumps({
                "type": "websocket.chat_and_inbox_messages",
                "consumer": "chat_consumer",
            })
        )
