from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from apps.chat.models.chat import Message
from apps.moderator.serializers.chat import (
    ModeratorMessageSerializer,
)
from apps.shared.permissions.admin import IsAdmin
from apps.shared.pagination.custom import CustomPagination


class ModeratorMessageView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorMessageSerializer

    def get_queryset(self):
        return Message.objects.all()

    def get(self, request):
        search = request.query_params.get("search")
        is_admin = request.query_params.get("is_admin")
        is_sent = request.query_params.get("is_sent")
        queryset = self.get_queryset()
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(chat__name__icontains=search_term)
                    | Q(sender__name__icontains=search_term)
                    | Q(sender__phone__icontains=search_term)
                    | Q(message__icontains=search_term)
                )
            queryset = queryset.filter(query)
        if is_admin is not None:
            queryset = queryset.filter(is_admin=is_admin)
        if is_sent is not None:
            queryset = queryset.filter(is_sent=is_sent)

        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
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
