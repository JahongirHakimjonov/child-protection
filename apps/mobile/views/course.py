from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.course import (
    Course,
    CourseLesson,
    CourseLessonResource,
    CourseCategory,
)
from apps.mobile.serializers.course import (
    CourseSerializer,
    CourseLessonSerializer,
    CourseLessonResourceSerializer,
    CourseCategorySerializer,
)


class CourseCategoryListAPIView(APIView):
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseCategory.objects.filter(is_active=True)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Course categories fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CourseListAPIView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: CourseSerializer(many=True)},
    )
    def get(self, request):
        category_id = request.query_params.get("category_id")
        if not category_id:
            return Response(
                {
                    "success": False,
                    "message": "category_id is required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.get_queryset().filter(category_id=category_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Courses fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CourseDetailAPIView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: CourseSerializer(many=True)},
    )
    def get(self, request, pk):
        category_id = request.query_params.get("category_id")
        if not category_id:
            return Response(
                {
                    "success": False,
                    "message": "category_id is required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.get_queryset()
        course = queryset.filter(id=pk, category_id=category_id).first()
        if course:
            serializer = self.serializer_class(course)
            return Response(
                {
                    "success": True,
                    "message": "Course fetched successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": "Course not found", "data": {}},
            status=status.HTTP_404_NOT_FOUND,
        )


class CourseLessonListAPIView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseLesson.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="course_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: CourseLessonSerializer(many=True)},
    )
    def get(self, request):
        course_id = request.query_params.get("course_id")
        if not course_id:
            return Response(
                {
                    "success": False,
                    "message": "course_id is required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.get_queryset().filter(course_id=course_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Course lessons fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CourseLessonDetailAPIView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseLesson.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="course_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: CourseLessonSerializer(many=True)},
    )
    def get(self, request, pk):
        course_id = request.query_params.get("course_id")
        if not course_id:
            return Response(
                {
                    "success": False,
                    "message": "course_id is required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.get_queryset()
        course_lesson = queryset.filter(id=pk, course_id=course_id).first()
        if course_lesson:
            serializer = self.serializer_class(course_lesson)
            return Response(
                {
                    "success": True,
                    "message": "Course lesson fetched successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": "Course lesson not found", "data": {}},
            status=status.HTTP_404_NOT_FOUND,
        )


class CourseLessonResourceListAPIView(APIView):
    serializer_class = CourseLessonResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseLessonResource.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="lesson_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: CourseLessonResourceSerializer(many=True)},
    )
    def get(self, request):
        lesson_id = request.query_params.get("lesson_id")
        if not lesson_id:
            return Response(
                {
                    "success": False,
                    "message": "lesson_id is required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.get_queryset().filter(lesson_id=lesson_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Course lesson resources fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CourseLessonResourceDetailAPIView(APIView):
    serializer_class = CourseLessonResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseLessonResource.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="lesson_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: CourseLessonResourceSerializer(many=True)},
    )
    def get(self, request, pk):
        lesson_id = request.query_params.get("lesson_id")
        if not lesson_id:
            return Response(
                {
                    "success": False,
                    "message": "lesson_id is required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.get_queryset()
        course_lesson_resource = queryset.filter(id=pk, lesson_id=lesson_id).first()
        if course_lesson_resource:
            serializer = self.serializer_class(course_lesson_resource)
            return Response(
                {
                    "success": True,
                    "message": "Course lesson resource fetched successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Course lesson resource not found",
                "data": {},
            },
            status=status.HTTP_404_NOT_FOUND,
        )
