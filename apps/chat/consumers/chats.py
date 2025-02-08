import json
import os

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken

from apps.chat.models.chat import Message
from apps.users.models.users import User

REDIS_URL = os.getenv("REDIS_CACHE_URL")


class ChatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handles WebSocket connection and immediately sends all messages.
        """
        # Authenticate user
        self.user = await self.authenticate_user()
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        # Join the global chat group
        self.room_group_name = "global_chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send all messages
        await self.send_all_messages()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Fetch and send all messages from the database.
        """
        await self.send_all_messages()

    @database_sync_to_async
    def authenticate_user(self):
        """
        Authenticate the user using the JWT token from query parameters.
        """
        try:
            token = self.scope["query_string"].decode().split("=")[1]
            validated_token = UntypedToken(token)
            user_id = validated_token["user_id"]
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()

    @database_sync_to_async
    def get_all_messages(self):
        """
        Fetch all messages from the database.
        """
        return list(
            Message.objects.filter(is_admin=False, is_received=False).order_by(
                "created_at"
            )
        )

    @database_sync_to_async
    def serialize_message(self, message):
        """
        Convert a message object to a dictionary.
        """
        return {
            "id": message.id,
            "sender": {
                "id": message.sender.id,
                "first_name": message.sender.first_name,
                "last_name": message.sender.last_name,
                "phone": message.sender.phone,
                "avatar": message.sender.avatar.url if message.sender.avatar else None,
            },
            "message": message.message,
            "file": (
                {
                    "id": message.file.id,
                    "name": message.file.name,
                    "file": message.file.file.url,
                    "size": message.file.size,
                    "type": message.file.type,
                    "created_at": message.file.created_at.isoformat(),
                }
                if message.file
                else None
            ),
            "is_admin": message.is_admin,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat(),
        }

    async def send_all_messages(self):
        """
        Fetch and send all messages to the WebSocket.
        """
        messages = await self.get_all_messages()
        for message in messages:
            message_data = await self.serialize_message(message)
            await self.send(text_data=json.dumps(message_data))
            message_id = message_data["id"]
            await self.make_message_is_recieved(message_id)

    async def send_message(self, event):
        """
        Send a new message in real-time when it's created.
        """
        message_id = event["message_id"]
        message = await self.get_message_by_id(message_id)

        if message:
            message_data = await self.serialize_message(message)
            await self.send(text_data=json.dumps(message_data))
            await self.make_message_is_recieved(message_id)

    @database_sync_to_async
    def get_message_by_id(self, message_id):
        """
        Fetch a single message by ID.
        """
        return Message.objects.filter(id=message_id).first()

    @database_sync_to_async
    def make_message_is_recieved(self, message_id):
        """
        Mark the message as received.
        """
        message = Message.objects.filter(id=message_id).first()
        message.is_received = True
        message.save()
        return message
