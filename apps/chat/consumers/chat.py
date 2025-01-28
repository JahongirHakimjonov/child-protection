import json
import os

import aioredis
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken

from apps.chat.models.chat import ChatRoom, Message
from apps.users.models import User, RoleChoices

REDIS_URL = os.getenv("REDIS_CACHE_URL")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_id = self.scope["url_route"]["kwargs"]["chat_room_id"]
        self.room_group_name = f"chat_{self.chat_room_id}"

        # Authenticate user
        self.user = await self.authenticate_user()
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        # Check if chat room exists and user is a participant
        if not await self.is_valid_chat():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Save user connection status
        await self.set_user_connection_status(self.user.id, True)

        # Send unsent messages
        await self.send_unsent_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Remove user connection status
        await self.set_user_connection_status(self.user.id, False)

    async def receive(self, text_data):
        """
        Receive a message from the WebSocket and process it.
        """
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get("message")
        file = text_data_json.get("file")

        if self.user.role == RoleChoices.ADMIN:
            is_admin = True
        else:
            is_admin = False

        # Validate file value
        if file is not None:
            try:
                file = int(file)
            except ValueError:
                await self.send(
                    text_data=json.dumps(
                        {"success": False, "message": "Invalid file ID"}
                    )
                )
                return

        # Save message to database
        message = await self.save_message(message_content, file, is_admin)

        # Send message to room group
        await self.send_message_to_group(message, self.channel_name)

        # Mark message as sent if both users are connected
        await self.update_message_status(message)

    async def chat_message(self, event):
        """
        Send a message to WebSocket.
        """
        # Skip sending the message to the sender if sender_channel_name matches
        # if self.channel_name != event["sender_channel_name"]:
        await self.send(text_data=json.dumps(event["message"]))

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
    def is_valid_chat(self):
        """
        Check if the chat room exists and the user is a participant.
        """
        try:
            chat_room = ChatRoom.objects.get(id=self.chat_room_id)
            return chat_room.participants.filter(id=self.user.id).exists()
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content, file, is_admin):
        """
        Save the message to the database.
        """
        chat_room = ChatRoom.objects.get(id=self.chat_room_id)
        file = file if file else None
        return Message.objects.create(
            chat=chat_room,
            sender=self.user,
            message=content,
            file_id=file,
            is_admin=is_admin,
            is_sent=False,  # Set is_sent to False for new messages
        )

    @database_sync_to_async
    def get_unsent_messages(self):
        """
        Get unsent messages from the database.
        """
        return list(Message.objects.filter(chat_id=self.chat_room_id, is_sent=False))

    @database_sync_to_async
    def get_message_sender(self, message):
        """
        Get the sender of the message.
        """
        return {
            "id": str(message.sender.id),
            "first_name": message.sender.first_name,
            "last_name": message.sender.last_name,
            "phone": message.sender.phone,
            "avatar": message.sender.avatar.url if message.sender.avatar else None,
        }

    async def send_unsent_messages(self):
        """
        Send unsent messages to the WebSocket.
        """
        unsent_messages = await self.get_unsent_messages()
        for message in unsent_messages:
            await self.send_message_to_group(message, None)
            # Mark message as sent if both users are connected
            await self.update_message_status(message)

    async def send_message_to_group(self, message, sender_channel_name):
        """
        Send a message to the room group.
        """
        chat_room_id = await database_sync_to_async(lambda: message.chat.id)()
        file = await database_sync_to_async(
            lambda: (
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
            )
        )()
        chat_room = await database_sync_to_async(lambda: message.chat)()
        participants = await database_sync_to_async(
            lambda: list(chat_room.participants.all())
        )()
        participants_data = [
            {
                "id": participant.id,
                "phone": participant.phone,
                "email": participant.email,
                "first_name": participant.first_name,
                "last_name": participant.last_name,
                "avatar": participant.avatar.url if participant.avatar else None,
                "role": participant.role,
                "created_at": participant.created_at.isoformat(),
                "updated_at": participant.updated_at.isoformat(),
            }
            for participant in participants
        ]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "id": message.id,
                    "chat": {
                        "id": chat_room.id,
                        "name": chat_room.name,
                        "participants": participants_data,
                        "created_at": chat_room.created_at.isoformat(),
                        "updated_at": chat_room.updated_at.isoformat(),
                    },
                    "sender": await self.get_message_sender(message),
                    "message": message.message,
                    "file": file,
                    "is_admin": message.is_admin,
                    "is_sent": message.is_sent,
                    "is_my": False,
                    "created_at": message.created_at.isoformat(),
                    "updated_at": message.updated_at.isoformat(),
                },
                "sender_channel_name": sender_channel_name,
            },
        )

    async def update_message_status(self, message):
        """
        Update the message status if both users are connected.
        """
        chat_room = await database_sync_to_async(
            lambda: ChatRoom.objects.get(id=self.chat_room_id)
        )()
        participants = await database_sync_to_async(
            lambda: list(chat_room.participants.all())
        )()
        connected_users = []

        for participant in participants:
            is_connected = await self.is_user_connected(participant.id)
            if is_connected:
                connected_users.append(participant.id)

        if len(connected_users) == len(participants):
            message.is_sent = True
            await database_sync_to_async(message.save)()

    async def is_user_connected(self, user_id):
        """
        Check if a user is connected to the WebSocket.
        """
        redis = aioredis.from_url(REDIS_URL)
        is_connected = await redis.get(f"user_{user_id}_connected")
        await redis.close()
        return is_connected == b"True"

    async def set_user_connection_status(self, user_id, status):
        """
        Set the user's connection status in Redis.
        """
        redis = aioredis.from_url(REDIS_URL)
        await redis.set(f"user_{user_id}_connected", "True" if status else "False")
        await redis.close()
