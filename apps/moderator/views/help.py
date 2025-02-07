from django.db.models import F, Window
from django.db.models import Q
from django.db.models.functions import RowNumber
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.help import Help
from apps.moderator.serializers.help import ModeratorHelpSerializer
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class ModeratorHelpView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorHelpSerializer

    def get_queryset(self):
        return (
            Help.objects.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('user'), F('status')],
                    order_by=F('created_at').desc()
                )
            )
            .filter(row_number=1)
        )

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
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

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

    @extend_schema(
        operation_id="moderator_help_detail_get",
    )
    def get(self, request, pk):
        help_object = Help.objects.filter(user_id=pk).order_by("-created_at")
        serializer = self.serializer_class(help_object, many=True)
        return Response(
            {
                "success": True,
                "message": "Help detail",
                "data": serializer.data,
            }
        )
