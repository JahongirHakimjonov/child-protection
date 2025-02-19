from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.course import CourseCategory, CourseLessonResource, CourseLesson
from apps.moderator.serializers.course import (
    ModeratorCourseCategorySerializer,
    ModeratorLessonResourceSerializer,
    ModeratorCourseLessonSerializer,
    ModeratorCourseCategoryDetailSerializer,
    ModeratorLessonResourceDetailSerializer,
    ModeratorCourseLessonDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class ModeratorCourseCategoryView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return CourseCategory.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorCourseCategorySerializer
        return ModeratorCourseCategoryDetailSerializer

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        queryset = self.get_queryset()

        tf = {"true": True, "false": False}
        if is_active is not None:
            queryset = queryset.filter(is_active=tf.get(is_active.lower(), None))
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(title__icontains=search_term)
                    | Q(sub_title__icontains=search_term)
                    | Q(description__icontains=search_term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseCategory created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorCourseCategoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorCourseCategoryDetailSerializer

    @extend_schema(
        operation_id="moderator_course_detail_get",
    )
    def get(self, request, pk):
        course_category = get_object_or_404(CourseCategory, pk)
        serializer = self.serializer_class(course_category)
        return Response(
            {
                "success": True,
                "message": "CourseCategory detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_course_detail_patch",
    )
    def patch(self, request, pk):
        course_category = get_object_or_404(CourseCategory, pk)
        serializer = self.serializer_class(course_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseCategory updated",
                    "data": serializer.data,
                }
            )
        return Response(
            {"success": False, "message": "Error", "data": serializer.errors}
        )

    @extend_schema(
        operation_id="moderator_course_detail_delete",
    )
    def delete(self, request, pk):
        course_category = get_object_or_404(CourseCategory, pk)
        course_category.delete()
        return Response({"success": True, "message": "CourseCategory deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
class ModeratorCourseLessonResourceView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return CourseLessonResource.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorLessonResourceSerializer
        return ModeratorLessonResourceDetailSerializer

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        lesson = request.query_params.get("lesson")
        queryset = self.get_queryset()

        tf = {"true": True, "false": False}
        if lesson:
            queryset = queryset.filter(lesson_id=lesson)
        if is_active is not None:
            queryset = queryset.filter(is_active=tf.get(is_active.lower(), None))
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(title__icontains=search_term)
                    | Q(description__icontains=search_term)
                    | Q(name__icontains=search_term)
                    | Q(lesson__title__icontains=search_term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseLessonResource created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorCourseLessonResourceDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorLessonResourceDetailSerializer

    @extend_schema(
        operation_id="moderator_category_lesson_resource_detail_get",
    )
    def get(self, request, pk):
        course_lesson_resource = get_object_or_404(CourseLessonResource, pk)
        serializer = self.serializer_class(course_lesson_resource)
        return Response(
            {
                "success": True,
                "message": "CourseLessonResource detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_category_lesson_resource_detail_patch",
    )
    def patch(self, request, pk):
        course_lesson_resource = get_object_or_404(CourseLessonResource, pk)
        serializer = self.serializer_class(
            course_lesson_resource, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseLessonResource updated",
                    "data": serializer.data,
                }
            )
        return Response(
            {"success": False, "message": "Error", "data": serializer.errors}
        )

    @extend_schema(
        operation_id="moderator_category_lesson_resource_detail_delete",
    )
    def delete(self, request, pk):
        course_lesson_resource = get_object_or_404(CourseLessonResource, pk=pk)
        course_lesson_resource.delete()
        return Response({"success": True, "message": "CourseLessonResource deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
class ModeratorCourseLessonView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return CourseLesson.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorCourseLessonSerializer
        return ModeratorCourseLessonDetailSerializer

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        category = request.query_params.get("category")
        queryset = self.get_queryset()

        tf = {"true": True, "false": False}
        if category:
            queryset = queryset.filter(category_id=category)
        if is_active is not None:
            queryset = queryset.filter(is_active=tf.get(is_active.lower(), None))
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(title__icontains=search_term)
                    | Q(description__icontains=search_term)
                    | Q(text__icontains=search_term)
                    | Q(category__title__icontains=search_term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseLesson created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorCourseLessonDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorCourseLessonDetailSerializer

    @extend_schema(
        operation_id="moderator_category_lesson_detail_get",
    )
    def get(self, request, pk):
        course_lesson = get_object_or_404(CourseLesson, pk)
        serializer = self.serializer_class(course_lesson)
        return Response(
            {
                "success": True,
                "message": "CourseLesson detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_category_lesson_detail_patch",
    )
    def patch(self, request, pk):
        course_lesson = get_object_or_404(CourseLesson, pk)
        serializer = self.serializer_class(
            course_lesson, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseLesson updated",
                    "data": serializer.data,
                }
            )
        return Response(
            {"success": False, "message": "Error", "data": serializer.errors}
        )

    @extend_schema(
        operation_id="moderator_category_lesson_detail_delete",
    )
    def delete(self, request, pk):
        course_lesson = get_object_or_404(CourseLesson, pk)
        course_lesson.delete()
        return Response({"success": True, "message": "CourseLesson deleted"})
