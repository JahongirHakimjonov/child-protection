from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.banner import Banner
from apps.moderator.serializers.banner import ModeratorBannerSerializer
from apps.shared.permissions.admin import IsAdmin
from apps.shared.pagination.custom import CustomPagination


class ModeratorBannerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorBannerSerializer

    def get_queryset(self):
        return Banner.objects.all()

    def get(self, request):
        is_active = request.query_params.get("is_active")
        queryset = self.get_queryset()
        if is_active is not None:
            queryset.filter(is_active=is_active)
        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Banner list",
                "data": serializer.data,
            }
        )

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

    def get_object(self, pk):
        try:
            return Banner.objects.get(pk=pk)
        except Banner.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Banner does not exist",
                }
            )

    def get(self, request, pk):
        banner = self.get_object(pk)
        serializer = self.serializer_class(banner)
        return Response(
            {
                "success": True,
                "message": "Banner detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        banner = self.get_object(pk)
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

    def delete(self, request, pk):
        banner = self.get_object(pk)
        banner.delete()
        return Response(
            {
                "success": True,
                "message": "Banner deleted",
            }
        )
