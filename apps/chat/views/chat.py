from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models.chat import ChatRoom, ChatResource
from apps.chat.serializers.chat import (
    ChatRoomSerializer,
    MessageSerializer,
    ChatResourceSerializer,
)
from apps.users.models import RoleChoices, User


class ChatRoomList(APIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        if user.role == RoleChoices.ADMIN:
            chat_rooms = ChatRoom.objects.all()
        else:
            chat_rooms = ChatRoom.objects.filter(participants=user)
            admins = User.objects.filter(role=RoleChoices.ADMIN)
            if not chat_rooms.exists():
                chat_room = ChatRoom.objects.create(name=f"Chat for {user.id}")
                chat_room.participants.add(user)
                chat_rooms = [chat_room]
                for admin in admins:
                    chat_room.participants.add(admin)

        serializer = self.serializer_class(chat_rooms, many=True)
        return Response(
            {
                "success": True,
                "message": "Chat rooms fetched successfully.",
                "data": serializer.data,
            }
        )


class MessageList(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id, format=None):
        user = request.user
        try:
            chat_room = ChatRoom.objects.get(id=chat_id)
        except ChatRoom.DoesNotExist:
            return Response({"success": False, "message": "Chat not found"})

        if (
            user.role == RoleChoices.ADMIN
            or chat_room.participants.filter(id=user.id).exists()
        ):
            messages = chat_room.messages.all()
            serializer = self.serializer_class(
                messages, many=True, context={"rq": request}
            )
            return Response(
                {
                    "success": True,
                    "message": "Messages fetched successfully.",
                    "data": serializer.data,
                }
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to view these messages.",
                    "data": [],
                },
                status=403,
            )


class ChatResourceView(APIView):
    serializer_class = ChatResourceSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        file = request.data.get("file")
        if not file:
            return Response(
                {"success": False, "message": "File is required."},
                status=400,
            )

        chat_resource = ChatResource.objects.create(
            user=user,
            file=file,
        )
        serializer = self.serializer_class(chat_resource)
        return Response(
            {
                "success": True,
                "message": "File uploaded successfully.",
                "data": serializer.data,
            }
        )
