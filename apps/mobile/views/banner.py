from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.banner import Banner
from apps.mobile.serializers.banner import BannerSerializer


class BannerListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banner.objects.filter(is_active=True)

    def get(self, request):
        banners = self.get_queryset()
        serializer = self.serializer_class(banners, many=True)
        return Response(
            {
                "success": True,
                "message": "Banners fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
