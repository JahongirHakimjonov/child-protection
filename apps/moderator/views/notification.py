from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from apps.users.models.notification import Notification

from apps.moderator.serializers.notification import ModeratorNotificationSerializer
from apps.shared.permissions.admin import IsAdmin
from apps.shared.pagination.custom import CustomPagination


class ModeratorNotificationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorNotificationSerializer

    def get_queryset(self):
        return Notification.objects.all()

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        is_read = request.query_params.get("is_read")
        queryset = self.get_queryset()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(user__phone__icontains=search_term)
                    | Q(user__username__icontains=search_term)
                    | Q(title__icontains=search_term)
                    | Q(message__icontains=search_term)
                )

        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
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
