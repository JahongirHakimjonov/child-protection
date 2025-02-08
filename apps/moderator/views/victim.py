from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.victim import VictimType, Victim, VictimStatus
from apps.moderator.serializers.victim import (
    ModeratorVictimTypeSerializer,
    ModeratorVictimTypeDetailSerializer,
    ModeratorVictimSerializer,
    ModeratorVictimStatusSerializer,
    ModeratorVictimStatusDetailSerializer,
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
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(operation_id="moderator_victim_type_post")
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Victim Type created",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": "Victim Type not created",
                "data": serializer.errors,
            }
        )


class VictimTypeDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorVictimTypeDetailSerializer

    @extend_schema(operation_id="moderator_victim_type_detail_get")
    def get(self, request, pk):
        victim_type = get_object_or_404(VictimType, pk=pk)
        serializer = self.serializer_class(victim_type)
        return Response(
            {"success": True, "message": "Victim Type found", "data": serializer.data}
        )

    @extend_schema(operation_id="moderator_victim_type_detail_patch")
    def patch(self, request, pk):
        victim_type = get_object_or_404(VictimType, pk=pk)
        serializer = self.serializer_class(victim_type, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "message": "Victim Type updated", "data": serializer.data}
        )

    @extend_schema(operation_id="moderator_victim_type_detail_delete")
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
        search = request.query_params.get("search")
        status = request.query_params.get("status")
        queryset = self.get_queryset()
        if status:
            queryset = queryset.filter(status_id=status)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= Q(message__icontains=search_term)
            queryset = queryset.filter(query)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class VictimDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorVictimSerializer

    @extend_schema(operation_id="moderator_victim_detail_get")
    def get(self, request, pk):
        victim = get_object_or_404(Victim, pk=pk)
        serializer = self.serializer_class(victim)
        return Response(
            {"success": True, "message": "Victim found", "data": serializer.data}
        )

    @extend_schema(operation_id="moderator_victim_detail_patch")
    def patch(self, request, pk):
        victim = get_object_or_404(Victim, pk=pk)
        serializer = self.serializer_class(victim, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "message": "Victim updated", "data": serializer.data}
        )

    @extend_schema(operation_id="moderator_victim_detail_delete")
    def delete(self, request, pk):
        victim = get_object_or_404(Victim, pk=pk)
        victim.delete()
        return Response(
            {
                "success": True,
                "message": "Victim deleted",
            }
        )


class VictimStatusList(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = CustomPagination

    def get_queryset(self):
        return VictimStatus.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorVictimStatusSerializer
        return ModeratorVictimStatusDetailSerializer

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
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(operation_id="moderator_victim_status_post")
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Victim Status created",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": "Victim Status not created",
                "data": serializer.errors,
            }
        )


class VictimStatusDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorVictimStatusDetailSerializer

    @extend_schema(operation_id="moderator_victim_status_detail_get")
    def get(self, request, pk):
        victim_status = get_object_or_404(VictimStatus, pk=pk)
        serializer = self.serializer_class(victim_status)
        return Response(
            {"success": True, "message": "Victim Status found", "data": serializer.data}
        )

    @extend_schema(operation_id="moderator_victim_status_detail_patch")
    def patch(self, request, pk):
        victim_status = get_object_or_404(VictimStatus, pk=pk)
        serializer = self.serializer_class(
            victim_status, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Victim Status updated",
                "data": serializer.data,
            }
        )

    @extend_schema(operation_id="moderator_victim_status_detail_delete")
    def delete(self, request, pk):
        victim_status = get_object_or_404(VictimStatus, pk=pk)
        victim_status.delete()
        return Response(
            {
                "success": True,
                "message": "Victim Status deleted",
            }
        )
