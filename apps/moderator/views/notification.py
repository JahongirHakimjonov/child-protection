from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models.notification import Notification

from apps.moderator.serializers.notification import ModeratorNotificationSerializer
from apps.shared.permissions.admin import IsAdmin


class ModeratorNotificationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorNotificationSerializer

    def get_queryset(self):
        return Notification.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset, many=True)
        return Response(
            {"success": True, "message": "Notification list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Notification created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorNotificationDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorNotificationSerializer

    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response(
                {"success": False, "message": "Notification does not exist"}
            )

    def get(self, request, pk):
        notification = self.get_object(pk=pk)
        serializer = self.serializer_class(data=notification)
        return Response(
            {
                "success": True,
                "message": "Notification detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        notification = self.get_object(pk=pk)
        serializer = self.serializer_class(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Notification updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "Notification does not exist"})

    def delete(self, request, pk):
        notification = self.get_object(pk=pk)
        notification.delete()
        return Response({"success": True, "message": "Notification deleted"})
