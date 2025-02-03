from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models.chat import ChatResource, ChatRoom, Message
from apps.moderator.serializers.chat import (
    ModeratorChatResourceSerializer,
    ModeratorChatRoomSerializer,
    ModeratorMessageSerializer,
)
from apps.shared.permissions.admin import IsAdmin


class ModeratorChatResourceView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorChatResourceSerializer

    def get_queryset(self):
        return ChatResource.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset, many=True)
        return Response(
            {"success": True, "message": "ChatResource list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "ChatResource created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorChatResourceDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorChatResourceSerializer

    def get_object(self, pk):
        try:
            return ChatResource.objects.get(pk=pk)
        except ChatResource.DoesNotExist:
            return Response(
                {"success": False, "message": "ChatResource does not exist"}
            )

    def get(self, request, pk):
        chatresource = self.get_object(pk=pk)
        serializer = self.serializer_class(data=chatresource)
        return Response(
            {
                "success": True,
                "message": "ChatResource detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        chatresource = self.get_object(pk=pk)
        serializer = self.serializer_class(chatresource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "ChatResource updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "ChatResource does not exist"})

    def delete(self, request, pk):
        chatresource = self.get_object(pk=pk)
        chatresource.delete()
        return Response({"success": True, "message": "ChatResource deleted"})


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


class ModeratorChatRoomView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(
            {"success": True, "message": "ChatRoom list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "ChatRoom created",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": serializer.errors})


class ModeratorChatRoomDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorChatRoomSerializer

    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            return Response({"success": False, "message": "ChatRoom does not exist"})

    def get(self, request, pk):
        chatroom = self.get_object(pk)
        serializer = self.serializer_class(chatroom)
        return Response(
            {"success": True, "message": "ChatRoom detail", "data": serializer.data}
        )

    def patch(self, request, pk):
        chatroom = self.get_object(pk)
        serializer = self.serializer_class(chatroom, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "ChatRoom updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": serializer.errors})

    def delete(self, request, pk):
        chatroom = self.get_object(pk)
        chatroom.delete()
        return Response({"success": True, "message": "ChatRoom deleted"})


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


class ModeratorMessageView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorMessageSerializer

    def get_queryset(self):
        return Message.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(
            {"success": True, "message": "Message list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Message created",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": serializer.errors})


class ModeratorMessageDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorMessageSerializer

    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"success": False, "message": "Message does not exist"})

    def get(self, request, pk):
        message = self.get_object(pk)
        serializer = self.serializer_class(message)
        return Response(
            {"success": True, "message": "Message detail", "data": serializer.data}
        )

    def patch(self, request, pk):
        message = self.get_object(pk)
        serializer = self.serializer_class(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Message updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": serializer.errors})

    def delete(self, request, pk):
        message = self.get_object(pk)
        message.delete()
        return Response({"success": True, "message": "Message deleted"})
