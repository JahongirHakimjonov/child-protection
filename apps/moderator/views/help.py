from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from apps.mobile.models.help import Help

from apps.moderator.serializers.help import ModeratorHelpSerializer
from apps.shared.permissions.admin import IsAdmin
from apps.shared.pagination.custom import CustomPagination


class ModeratorHelpView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorHelpSerializer

    def get_queryset(self):
        return Help.objects.all()

    def get(self, request):
        search = request.query_params.get("search")
        queryset = self.get_queryset()
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(user__username__icontains=search_term)
                    | Q(user__phone__icontains=search_term)
                    | Q(status__icontains=search_term)
                )
        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return Response(
            {"success": True, "message": "Help list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Help created", "data": serializer.data}
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorHelpDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorHelpSerializer

    def get_object(self, pk):
        try:
            return Help.objects.get(pk=pk)
        except Help.DoesNotExist:
            return Response({"success": False, "message": "Help does not exist"})

    def get(self, request, pk):
        help_object = self.get_object(pk=pk)
        serializer = self.serializer_class(data=help_object)
        return Response(
            {
                "success": True,
                "message": "Help detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        help_object = self.get_object(pk=pk)
        serializer = self.serializer_class(help_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Help updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "Help does not exist"})

    def delete(self, request, pk):
        help_object = self.get_object(pk=pk)
        help_object.delete()
        return Response({"success": True, "message": "Help deleted"})
