from rest_framework import serializers

from apps.chat.models.chat import ChatRoom, Message, ChatResource
from apps.users.serializers.me import UserSerializer


class ChatResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatResource
        fields = (
            "id",
            "name",
            "file",
            "size",
            "type",
            "created_at",
        )


class MessageLastSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    file = ChatResourceSerializer(read_only=True)

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


class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = MessageLastSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "name",
            "message_count",
            "last_message",
            "created_at",
            "updated_at",
        )


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatRoomSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    file = ChatResourceSerializer(read_only=True)

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
