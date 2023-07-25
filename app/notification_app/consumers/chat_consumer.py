import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

from notification_app.methods.chat_methods import create_or_update_inbox_participant, get_participants, remove_channel_layer, save_channel_layer


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
                self.scope["user"].id, self.channel_name)
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

        # await self.channel_layer.add(
        #     {
        #         "type": "websocket.???",
        #         "message": message
        #     }
        # )

    async def websocket_disconnect(self, message):
        await remove_channel_layer(self.scope["user"].id)
        raise StopConsumer()

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

    async def websocket_create_or_update_inbox_participant(self, message):
        """
        This method is used to create or update an 'InboxParticipant'-Entry after sending a message.
        """

        create_or_update_inbox_participant()

        await self.send(
            json.dumps({
                "type": "websocket.create_or_update_inbox_participant",
                "consumer": "chat_consumer",
                "message": message,
            })
        )
