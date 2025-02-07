from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.news import News
from apps.moderator.serializers.news import (
    ModeratorNewsSerializer,
    ModeratorNewsDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class ModeratorNewsList(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = CustomPagination

    def get_queryset(self):
        return News.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorNewsSerializer
        return ModeratorNewsDetailSerializer

    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "News created",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "News not created",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ModeratorNewsDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        return ModeratorNewsDetailSerializer

    @extend_schema(
        operation_id="news_detail_get",
    )
    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = self.get_serializer_class()(news)
        return Response(
            {
                "success": True,
                "message": "News detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="news_detail_patch",
    )
    def patch(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = self.get_serializer_class()(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "News updated",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": "News not updated",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        operation_id="news_detail_delete",
    )
    def delete(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response(
            {
                "success": True,
                "message": "News deleted",
            }
        )
