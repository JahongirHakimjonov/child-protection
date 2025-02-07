from django.db.models import F
from django.db.models.functions import Sqrt, Power, Sin, Cos, Radians
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.places import Place
from apps.mobile.serializers.places import PlaceSerializer
from apps.shared.pagination import CustomPagination


class PlacesView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Place.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="longitude", description="Longitude", required=False, type=float
            ),
            OpenApiParameter(
                name="latitude", description="Latitude", required=False, type=float
            ),
        ],
        responses={200: PlaceSerializer(many=True)},
    )
    def get(self, request):
        longitude = request.query_params.get("longitude")
        latitude = request.query_params.get("latitude")
        queryset = self.get_queryset()

        if longitude and latitude:
            longitude = float(longitude)
            latitude = float(latitude)
            queryset = queryset.annotate(
                distance=Sqrt(
                    Power(Sin(Radians(F("latitude") - latitude) / 2), 2)
                    + Cos(Radians(latitude))
                    * Cos(Radians(F("latitude")))
                    * Power(Sin(Radians(F("longitude") - longitude) / 2), 2)
                )
                * 2
                * 6371
            ).order_by("distance")

        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {"success": True, "message": "Place data fetched", "data": serializer.data}
        )
