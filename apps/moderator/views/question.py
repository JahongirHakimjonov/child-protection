from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from apps.mobile.models.question import QuestionCategory, Question
from apps.moderator.serializers.question import (
    ModeratorQuestionCategorySerializer,
    ModeratorQuestionSerializer,
)
from apps.shared.permissions.admin import IsAdmin
from apps.shared.pagination.custom import CustomPagination


class ModeratorQuestionCategoryView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorQuestionCategorySerializer

    def get_queryset(self):
        return QuestionCategory.objects.all()

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
                query &= Q(name__icontains=search_term)
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
                    "message": "QuestionCategory created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorQuestionCategoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorQuestionCategorySerializer

    def get(self, request, pk):
        questioncategory = get_object_or_404(QuestionCategory, pk)
        serializer = self.serializer_class(questioncategory)
        return Response(
            {
                "success": True,
                "message": "QuestionCategory detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        questioncategory = get_object_or_404(QuestionCategory, pk)
        serializer = self.serializer_class(questioncategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "QuestionCategory updated",
                    "data": serializer.data,
                }
            )
        return Response(
            {"success": False, "message": "QuestionCategory does not exist"}
        )

    def delete(self, request, pk):
        questioncategory = get_object_or_404(QuestionCategory, pk)
        questioncategory.delete()
        return Response({"success": True, "message": "QuestionCategory deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class ModeratorQuestionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorQuestionSerializer

    def get_queryset(self):
        return Question.objects.all()

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
                    Q(category__name__icontains=search_term)
                    | Q(sort_number__icontains=search_term)
                    | Q(title__icontains=search_term)
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
                    "message": "Question created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorQuestionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorQuestionCategorySerializer

    def get(self, request, pk):
        question = get_object_or_404(Question, pk)
        serializer = self.serializer_class(question)
        return Response(
            {
                "success": True,
                "message": "Question detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        question = get_object_or_404(Question, pk)
        serializer = self.serializer_class(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Question updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "Question does not exist"})

    def delete(self, request, pk):
        question = get_object_or_404(Question, pk)
        question.delete()
        return Response({"success": True, "message": "Question deleted"})
