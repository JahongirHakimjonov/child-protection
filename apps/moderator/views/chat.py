from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models.chat import ChatRoom, ChatResource, Message
from apps.moderator.serializers.chat import (
    ModeratorChatRoomSerializer,
    ModeratorMessageSerializer,
    ModeratorChatResourceSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.permissions.admin import IsAdmin
from apps.users.models.users import RoleChoices, User


class ModeratorChatRoomList(APIView):
    serializer_class = ModeratorChatRoomSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, format=None):
        user = request.user
        if user.role == RoleChoices.ADMIN or user.role == RoleChoices.SUPER_ADMIN:
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


class ModeratorMessageList(APIView):
    serializer_class = ModeratorMessageSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, format=None):
        user = request.user
        chat_id = request.query_params.get("chat_id")

        if user.role == RoleChoices.ADMIN or user.role == RoleChoices.SUPER_ADMIN:
            messages = Message.objects.filter(chat_id=chat_id)
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


class ModeratorMessageUpdate(APIView):
    serializer_class = ModeratorMessageSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk, format=None):
        user = request.user
        message = get_object_or_404(Message, pk=pk)

        if user.role == RoleChoices.ADMIN or user.role == RoleChoices.SUPER_ADMIN:
            serializer = self.serializer_class(
                message, data=request.data, partial=True, context={"rq": request}
            )
            if serializer.is_valid():
                serializer.save()
                message.chat.message_count = 0
                Message.objects.filter(chat=message.chat).update(is_read=True)
                message.chat.save()
                return Response(
                    {
                        "success": True,
                        "message": "Message updated successfully.",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Message could not be updated.",
                        "data": serializer.errors,
                    },
                    status=400,
                )
        else:
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to update this message.",
                    "data": [],
                },
                status=403,
            )


class ModeratorChatResourceView(APIView):
    serializer_class = ModeratorChatResourceSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

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
