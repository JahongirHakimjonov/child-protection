from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from apps.mobile.models.course import CourseCategory, CourseLessonResource, CourseLesson
from apps.moderator.serializers.course import (
    ModeratorCourseCategorySerializer,
    ModeratorLessonResourceSerializer,
    ModeratorCourseLessonSerializer,
)
from apps.shared.permissions.admin import IsAdmin
from apps.shared.pagination.custom import CustomPagination


class ModeratorCourseCategoryView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorCourseCategorySerializer

    def get_queryset(self):
        return CourseCategory.objects.all()

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
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
    serializer_class = ModeratorCourseCategorySerializer

    def get(self, request, pk):
        coursecategory = get_object_or_404(CourseCategory, pk)
        serializer = self.serializer_class(coursecategory)
        return Response(
            {
                "success": True,
                "message": "CourseCategory detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        coursecategory = get_object_or_404(CourseCategory, pk)
        serializer = self.serializer_class(coursecategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseCategory updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "CourseCategory does not exist"})

    def delete(self, request, pk):
        coursecategory = get_object_or_404(CourseCategory, pk)
        coursecategory.delete()
        return Response({"success": True, "message": "CourseCategory deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class ModeratorCourseLessonResourceView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorLessonResourceSerializer

    def get_queryset(self):
        return CourseLessonResource.objects.all()

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
                    | Q(description__icontains=search_term)
                    | Q(name__icontains=search_term)
                    | Q(lesson__title__icontains=search_term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
    serializer_class = ModeratorCourseLessonSerializer

    def get(self, request, pk):
        courselessonresource = get_object_or_404(CourseLessonResource, pk)
        serializer = self.serializer_class(courselessonresource)
        return Response(
            {
                "success": True,
                "message": "CourseLessonResource detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        courselessonresource = get_object_or_404(CourseLessonResource, pk)
        serializer = self.serializer_class(courselessonresource, data=request.data)
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
            {"success": False, "message": "CourseLessonResource does not exist"}
        )

    def delete(self, request, pk):
        courselessonresource = get_object_or_404(CourseLessonResource, pk)
        courselessonresource.delete()
        return Response({"success": True, "message": "CourseLessonResource deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class ModeratorCourseLessonView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorCourseLessonSerializer

    def get_queryset(self):
        return CourseLesson.objects.all()

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
                    | Q(description__icontains=search_term)
                    | Q(text__icontains=search_term)
                    | Q(category__title__icontains=search_term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
    serializer_class = ModeratorCourseLessonSerializer

    def get(self, request, pk):
        courselesson = get_object_or_404(CourseLesson, pk)
        serializer = self.serializer_class(courselesson)
        return Response(
            {
                "success": True,
                "message": "CourseLesson detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        courselesson = get_object_or_404(CourseLesson, pk)
        serializer = self.serializer_class(courselesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "CourseLesson updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "CourseLesson does not exist"})

    def delete(self, request, pk):
        courselesson = get_object_or_404(CourseLesson, pk)
        courselesson.delete()
        return Response({"success": True, "message": "CourseLesson deleted"})
