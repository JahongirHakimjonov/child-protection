from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.question import (
    Question,
    QuestionCategory,
)
from apps.mobile.serializers.question import (
    QuestionSerializer,
    QuestionCategorySerializer,
)


class QuestionCategoryListAPIView(APIView):
    serializer_class = QuestionCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuestionCategory.objects.filter(is_active=True)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Question categories fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class QuestionListAPIView(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(is_active=True)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category_id", description="Filter", required=False, type=int
            ),
        ],
        responses={200: QuestionSerializer(many=True)},
    )
    def get(self, request):
        category_id = request.query_params.get("category_id")
        if category_id:
            queryset = self.get_queryset().filter(category_id=category_id)
        else:
            queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Questions fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class QuestionDetailAPIView(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None

    def get(self, request, pk):
        question = self.get_object(pk)
        if question is None:
            return Response(
                {"success": False, "message": "Question not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(question)
        return Response(
            {
                "success": True,
                "message": "Question fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
