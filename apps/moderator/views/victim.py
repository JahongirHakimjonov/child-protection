from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.victim import VictimType, Victim
from apps.moderator.serializers.victim import (
    ModeratorVictimTypeSerializer,
    ModeratorVictimTypeDetailSerializer,
    ModeratorVictimSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class VictimTypeList(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = CustomPagination

    def get_queryset(self):
        return VictimType.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorVictimTypeSerializer
        return ModeratorVictimTypeDetailSerializer

    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class VictimTypeDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorVictimTypeDetailSerializer

    def get(self, request, pk):
        victim_type = get_object_or_404(VictimType, pk=pk)
        serializer = self.serializer_class(victim_type)
        return Response(
            {"success": True, "message": "Victim Type found", "data": serializer.data}
        )

    def patch(self, request, pk):
        victim_type = get_object_or_404(VictimType, pk=pk)
        serializer = self.serializer_class(victim_type, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "message": "Victim Type updated", "data": serializer.data}
        )

    def delete(self, request, pk):
        victim_type = get_object_or_404(VictimType, pk=pk)
        victim_type.delete()
        return Response(
            {
                "success": True,
                "message": "Victim Type deleted",
            }
        )


class VictimList(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Victim.objects.all()

    def get_serializer_class(self):
        return ModeratorVictimSerializer

    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class VictimDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorVictimSerializer

    def get(self, request, pk):
        victim = get_object_or_404(Victim, pk=pk)
        serializer = self.serializer_class(victim)
        return Response(
            {"success": True, "message": "Victim found", "data": serializer.data}
        )

    def patch(self, request, pk):
        victim = get_object_or_404(Victim, pk=pk)
        serializer = self.serializer_class(victim, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "message": "Victim updated", "data": serializer.data}
        )

    def delete(self, request, pk):
        victim = get_object_or_404(Victim, pk=pk)
        victim.delete()
        return Response(
            {
                "success": True,
                "message": "Victim deleted",
            }
        )
