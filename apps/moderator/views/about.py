from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.about import About, AboutProject
from apps.moderator.serializers.about import (
    ModeratorAboutSerializer,
    ModeratorAboutProjectSerializer,
    ModeratorAboutDetailSerializer,
    ModeratorAboutProjectDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.permissions.admin import IsAdmin


class ModeratorAboutView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return About.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorAboutSerializer
        return ModeratorAboutDetailSerializer

    def get(self, request):
        about = self.get_queryset()
        serializer = self.get_serializer_class()(about, many=True)
        return Response(
            {
                "success": True,
                "message": "About data retrieved successfully",
                "data": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "About data created successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": "About data not created",
                "data": serializer.errors,
            }
        )


class ModeratorAboutDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorAboutDetailSerializer

    @extend_schema(operation_id="about_detail_get")
    def get(self, request, pk):
        about = get_object_or_404(About, pk=pk)
        serializer = self.serializer_class(about)
        return Response(
            {
                "success": True,
                "message": "About data retrieved successfully",
                "data": serializer.data,
            }
        )

    @extend_schema(operation_id="about_detail_patch")
    def patch(self, request, pk):
        about = get_object_or_404(About, pk=pk)
        serializer = self.serializer_class(about, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "About data updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": "About data not updated",
                "data": serializer.errors,
            }
        )

    @extend_schema(operation_id="about_detail_delete")
    def delete(self, request, pk):
        about = get_object_or_404(About, pk=pk)
        about.delete()
        return Response({"success": True, "message": "About data deleted successfully"})


class ModeratorAboutProjectView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return AboutProject.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorAboutProjectSerializer
        return ModeratorAboutProjectDetailSerializer

    def get(self, request):
        about = self.get_queryset()
        serializer = self.get_serializer_class()(about, many=True)
        return Response(
            {
                "success": True,
                "message": "About project data retrieved successfully",
                "data": serializer.data,
            }
        )


class ModeratorAboutProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorAboutProjectDetailSerializer

    @extend_schema(operation_id="about_project_detail_get")
    def get(self, request, pk):
        about = get_object_or_404(AboutProject, pk=pk)
        serializer = self.serializer_class(about)
        return Response(
            {
                "success": True,
                "message": "About project data retrieved successfully",
                "data": serializer.data,
            }
        )

    @extend_schema(operation_id="about_project_detail_patch")
    def patch(self, request, pk):
        about = get_object_or_404(AboutProject, pk=pk)
        serializer = self.serializer_class(about, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "About project data updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {
                "success": False,
                "message": "About project data not updated",
                "data": serializer.errors,
            }
        )

    @extend_schema(operation_id="about_project_detail_delete")
    def delete(self, request, pk):
        about = get_object_or_404(AboutProject, pk=pk)
        about.delete()
        return Response(
            {"success": True, "message": "About project data deleted successfully"}
        )
