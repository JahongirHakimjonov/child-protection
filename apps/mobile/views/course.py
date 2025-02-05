from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.course import (
    CourseLesson,
    CourseLessonResource,
    CourseCategory,
    ResourceTypes,
)
from apps.mobile.models.saved import Viewed
from apps.mobile.serializers.course import (
    CourseLessonSerializer,
    CourseCategorySerializer,
    LessonResourceSerializer,
)
from apps.shared.pagination import CustomPagination


class CourseCategoryListAPIView(APIView):
    serializer_class = CourseCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CourseCategory.objects.filter(is_active=True)

    def get_progress_percent(self, category, user):
        viewed = category.courses.filter(viewed__user=user).count()
        total = category.courses.count()
        if total:
            return round(viewed / total * 100, 2)
        return 0

    def get(self, request):
        search = request.query_params.get("search")
        progress = request.query_params.get("progress")
        queryset = self.get_queryset()
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= (
                    Q(title__icontains=term)
                    | Q(sub_title__icontains=term)
                    | Q(description__icontains=term)
                )
            queryset = queryset.filter(query)
        if progress and progress.lower() == "true":
            user = request.user
            if user.is_authenticated:
                queryset = [
                    category
                    for category in queryset
                    if self.get_progress_percent(category, user) > 0
                ]
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)


class CourseCategoryDetailAPIView(APIView):
    serializer_class = CourseCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CourseCategory.objects.filter(is_active=True)

    @extend_schema(operation_id="course-category-detail")
    def get(self, request, pk):
        category = self.get_queryset().filter(id=pk).first()
        if category:
            serializer = self.serializer_class(category)
            return Response(
                {
                    "success": True,
                    "message": "Course category fetched successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Course category not found",
                "data": {},
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class LessonListAPIView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CourseLesson.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category_id", description="Filter", required=False, type=int
            ),
            OpenApiParameter(
                name="top",
                description="Filter",
                required=False,
                type=bool,
            ),
        ],
        responses={200: CourseLessonSerializer(many=True)},
    )
    def get(self, request):
        category_id = request.query_params.get("category_id")
        top = request.query_params.get("top")
        queryset = self.get_queryset()
        if category_id:
            queryset = self.get_queryset().filter(category_id=category_id)
        if top and top.lower() == "true":
            queryset = queryset.order_by("-likes_count")

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)


class LessonDetailAPIView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseLesson.objects.filter(is_active=True)

    @extend_schema(
        operation_id="course-lesson-detail",
        parameters=[
            OpenApiParameter(
                name="category_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: CourseLessonSerializer(many=True)},
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
            serializer = self.serializer_class(course, context={"rq": request})
            Viewed.objects.get_or_create(user=request.user, lesson=course)
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


class LessonResourceListAPIView(APIView):
    serializer_class = LessonResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseLessonResource.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="lesson_id", description="Filter", required=True, type=int
            ),
            OpenApiParameter(
                name="type",
                description="Filter",
                required=False,
                type=str,
                enum=[choice.value for choice in ResourceTypes],
            ),
        ],
        responses={200: LessonResourceSerializer(many=True)},
    )
    def get(self, request):
        lesson_id = request.query_params.get("lesson_id")
        type = request.query_params.get("type")
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
        if type:
            queryset = queryset.filter(type=type)
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Course lesson resources fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class LessonResourceDetailAPIView(APIView):
    serializer_class = LessonResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseLessonResource.objects.filter(is_active=True)

    @extend_schema(
        operation_id="course-resource-detail",
        parameters=[
            OpenApiParameter(
                name="lesson_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: LessonResourceSerializer(many=True)},
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
