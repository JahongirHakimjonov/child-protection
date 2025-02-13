from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.about import About, AboutProject
from apps.mobile.serializers.about import AboutSerializer, AboutProjectSerializer
from apps.shared.exceptions.http404 import get_object_or_404


class AboutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AboutSerializer

    def get_queryset(self):
        return About.objects.all()

    def get(self, request):
        about = self.get_queryset()
        serializer = self.serializer_class(about, many=True)
        return Response(
            {
                "success": True,
                "message": "About data retrieved successfully",
                "data": serializer.data,
            }
        )


class AboutDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AboutSerializer

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


class AboutProjectView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AboutProjectSerializer

    def get_queryset(self):
        return AboutProject.objects.all()

    def get(self, request):
        about = self.get_queryset()
        serializer = self.serializer_class(about, many=True)
        return Response(
            {
                "success": True,
                "message": "About project data retrieved successfully",
                "data": serializer.data,
            }
        )


class AboutProjectDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AboutProjectSerializer

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
