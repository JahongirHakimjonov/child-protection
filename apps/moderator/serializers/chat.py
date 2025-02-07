from rest_framework import serializers

from apps.chat.models.chat import ChatRoom, Message, ChatResource
from apps.users.serializers.me import UserSerializer


class ModeratorChatResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatResource
        fields = (
            "id",
            "user",
            "name",
            "file",
            "size",
            "type",
            "created_at",
        )


class ModeratorChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ("id", "name", "participants", "message_count", "last_message", "created_at", "updated_at")


class ModeratorMessageSerializer(serializers.ModelSerializer):
    chat = ModeratorChatRoomSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    file = ModeratorChatResourceSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "chat",
            "sender",
            "message",
            "file",
            "is_admin",
            "is_sent",
            "created_at",
            "updated_at",
        )
