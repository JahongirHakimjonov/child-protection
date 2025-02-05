from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.faq import FAQ
from apps.moderator.serializers.faq import (
    ModeratorFAQSerializer,
    ModeratorFAQDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class ModeratorFAQView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return FAQ.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorFAQSerializer
        return ModeratorFAQDetailSerializer

    def get(self, request):
        queryset = self.get_queryset()
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "FAQ created",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorFAQDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorFAQDetailSerializer

    @extend_schema(
        operation_id='moderator_faq',
    )
    def get(self, request, pk):
        faq = get_object_or_404(FAQ, pk)
        serializer = self.serializer_class(faq)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id='moderator_faq',
    )
    def patch(self, request, pk):
        faq = get_object_or_404(FAQ, pk)
        serializer = self.serializer_class(faq, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "FAQ updated",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )

    @extend_schema(
        operation_id='moderator_faq',
    )
    def delete(self, request, pk):
        faq = get_object_or_404(FAQ, pk)
        faq.delete()
        return Response(
            {
                "success": True,
                "message": "FAQ deleted",
            }
        )
