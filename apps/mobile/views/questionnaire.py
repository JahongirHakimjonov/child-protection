from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.questionnaire import (
    Questionnaire, QuestionnaireCategory

)
from apps.mobile.serializers.questionnaire import (
    QuestionnaireCategorySerializer,
    QuestionnaireSerializer,
    QuestionnaireUserAnswerSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination import CustomPagination


class QuestionnaireCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionnaireCategorySerializer

    def get_queryset(self):
        return QuestionnaireCategory.objects.filter(is_active=True)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Questionnaire categories fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)


class QuestionnaireView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionnaireSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Questionnaire.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category", description="Category", required=True, type=int
            ),
        ]
    )
    def get(self, request):
        queryset = self.get_queryset()
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class QuestionnaireDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionnaireSerializer

    def get(self, request, pk):
        queryset = get_object_or_404(Questionnaire, pk=pk, is_active=True)
        serializer = self.serializer_class(queryset)
        return Response(
            {
                "success": True,
                "message": "Questionnaire fetched successfully",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)


class QuestionnaireUserAnswerView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionnaireUserAnswerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "success": True,
                    "message": "Questionnaire answer submitted successfully",
                    "data": serializer.data,
                }, status=status.HTTP_201_CREATED)
        return Response(
            {
                "success": False,
                "message": "Questionnaire answer submission failed",
                "data": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
