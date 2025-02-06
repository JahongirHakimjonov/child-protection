from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.places import Place
from apps.moderator.serializers.places import (
    ModeratorPlaceSerializer,
    ModeratorPlaceDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.permissions.admin import IsAdmin


class ModeratorPlaceList(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Place.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorPlaceSerializer
        return ModeratorPlaceDetailSerializer

    def get(self, request):
        search = request.query_params.get("search")
        queryset = self.get_queryset()
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                        Q(name__icontains=search_term)
                        | Q(name_uz__icontains=search_term)
                        | Q(name_ru__icontains=search_term)
                        | Q(name_en__icontains=search_term)
                )
            queryset = queryset.filter(query)
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Place data fetched",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Place created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Place not created",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ModeratorPlaceDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorPlaceDetailSerializer

    @extend_schema(
        operation_id="moderator_place_detail_get",
    )
    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        serializer = self.serializer_class(place)
        return Response(
            {
                "success": True,
                "message": "Place found",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_place_detail_patch",
    )
    def put(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        serializer = self.serializer_class(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Place updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": "Place not updated",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        operation_id="moderator_place_detail_delete",
    )
    def delete(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        place.delete()
        return Response(
            {
                "success": True,
                "message": "Place deleted successfully",
            }
        )
