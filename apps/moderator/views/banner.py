from drf_spectacular.utils import extend_schema

from apps.shared.exceptions.http404 import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.banner import Banner
from apps.moderator.serializers.banner import ModeratorBannerSerializer
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class ModeratorBannerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorBannerSerializer

    def get_queryset(self):
        return Banner.objects.all()

    def get(self, request):
        is_active = request.query_params.get("is_active")
        queryset = self.get_queryset()
        tf = {"true": True, "false": False}
        if is_active is not None:
            queryset = queryset.filter(is_active=tf.get(is_active.lower(), None))
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
                {
                    "success": True,
                    "message": "Banner created",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorBannerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorBannerSerializer

    @extend_schema(
        operation_id="moderator_banner_detail_get",
    )
    def get(self, request, pk):
        banner = get_object_or_404(Banner, pk)
        serializer = self.serializer_class(banner)
        return Response(
            {
                "success": True,
                "message": "Banner detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_banner_detail_patch",
    )
    def patch(self, request, pk):
        banner = get_object_or_404(Banner, pk)
        serializer = self.serializer_class(banner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Banner updated",
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
        operation_id="moderator_banner_detail_delete",
    )
    def delete(self, request, pk):
        banner = get_object_or_404(Banner, pk)
        banner.delete()
        return Response(
            {
                "success": True,
                "message": "Banner deleted",
            }
        )
