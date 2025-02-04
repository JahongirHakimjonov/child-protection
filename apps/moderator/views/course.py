from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

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
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(title__icontains=search_term)
                    | Q(sub_title__icontains=search_term)
                    | Q(description__icontains=search_term)
                )

        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "CourseCategory list",
                "data": serializer.data,
            }
        )

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

    def get_object(self, pk):
        try:
            return CourseCategory.objects.get(pk=pk)
        except CourseCategory.DoesNotExist:
            return Response(
                {"success": False, "message": "CourseCategory does not exist"}
            )

    def get(self, request, pk):
        coursecategory = self.get_object(pk=pk)
        serializer = self.serializer_class(data=coursecategory)
        return Response(
            {
                "success": True,
                "message": "CourseCategory detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        coursecategory = self.get_object(pk=pk)
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
        coursecategory = self.get_object(pk=pk)
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
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
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
        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "CourseLessonResource list",
                "data": serializer.data,
            }
        )

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

    def get_object(self, pk):
        try:
            return CourseLessonResource.objects.get(pk=pk)
        except CourseLessonResource.DoesNotExist:
            return Response(
                {"success": False, "message": "CourseLessonResource does not exist"}
            )

    def get(self, request, pk):
        courselessonresource = self.get_object(pk=pk)
        serializer = self.serializer_class(data=courselessonresource)
        return Response(
            {
                "success": True,
                "message": "CourseLessonResource detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        courselessonresource = self.get_object(pk=pk)
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
        courselessonresource = self.get_object(pk=pk)
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
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
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
        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "CourseLesson list",
                "data": serializer.data,
            }
        )

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

    def get_object(self, pk):
        try:
            return CourseLesson.objects.get(pk=pk)
        except CourseLesson.DoesNotExist:
            return Response(
                {"success": False, "message": "CourseLesson does not exist"}
            )

    def get(self, request, pk):
        courselesson = self.get_object(pk=pk)
        serializer = self.serializer_class(data=courselesson)
        return Response(
            {
                "success": True,
                "message": "CourseLesson detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        courselesson = self.get_object(pk=pk)
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
        courselesson = self.get_object(pk=pk)
        courselesson.delete()
        return Response({"success": True, "message": "CourseLesson deleted"})
