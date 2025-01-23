import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken

from apps.chat.models.chat import ChatRoom, Message
from apps.users.models import User


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
        is_valid_chat = await self.is_valid_chat()
        if not is_valid_chat:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send unsent messages
        await self.send_unsent_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Receive a message from the WebSocket and process it.
        """
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get("message", None)
        file_url = text_data_json.get("file", None)
        is_admin = text_data_json.get("is_admin", False)

        # Save message to database
        message = await self.save_message(message_content, file_url, is_admin)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "sender": await self.get_message_sender(message),
                    "chat_room": str(message.chat.id),
                    "message": message.message,
                    "file": message.file.url if message.file else None,
                    "created_at": message.created_at.isoformat(),
                    "is_admin": message.is_admin,
                },
                "sender_channel_name": self.channel_name,
            },
        )

    async def chat_message(self, event):
        """
        Send a message to WebSocket.
        """
        # Skip sending the message to the sender if sender_channel_name matches
        if self.channel_name == event["sender_channel_name"]:
            return

        # Send the structured message to WebSocket
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
    def save_message(self, content, file_url, is_admin):
        """
        Save the message to the database.
        """
        chat_room = ChatRoom.objects.get(id=self.chat_room_id)
        if file_url:
            get_url_path = self.get_url_path(file_url)
        else:
            get_url_path = None
        return Message.objects.create(
            chat=chat_room,
            sender=self.user,
            message=content,
            file=get_url_path,
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
            chat_room_id = await database_sync_to_async(lambda: message.chat.id)()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": {
                        "sender": await self.get_message_sender(message),
                        "chat_room": str(chat_room_id),
                        "message": message.message,
                        "file": message.file.url if message.file else None,
                        "created_at": message.created_at.isoformat(),
                        "is_admin": message.is_admin,
                    },
                    "sender_channel_name": self.channel_name,  # Include sender_channel_name
                },
            )
            message.is_sent = True
            await database_sync_to_async(message.save)()

    async def get_url_path(self, url):
        """
        Get the relative URL path from the full URL.
        """
        return url.replace("http://testserver", "")
