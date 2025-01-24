from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.chat.models.chat import ChatRoom, Message, ChatResource
from apps.users.serializers import UserSerializer


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


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ("id", "name", "participants", "created_at", "updated_at")


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatRoomSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    is_my = serializers.SerializerMethodField()
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
            "is_my",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(serializers.BooleanField)
    def get_is_my(self, obj):
        request = self.context.get("rq")
        if obj.sender.id == request.user.id:
            return True
        return False
