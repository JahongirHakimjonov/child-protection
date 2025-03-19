from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.questionnaire import (
    Questionnaire,
    QuestionnaireCategory,
    QuestionnaireUserAnswer,
)
from apps.moderator.serializers.questionnaire import (
    ModeratorQuestionareCategorySerializer,
    ModeratorQuestionareCategoryDetailSerializer,
    ModeratorQuestionareSerializer,
    ModeratorQuestionareCreateSerializer,
    ModeratorQuestionnaireDetailSerializer,
    ModeratorQuestionareUserAnswerSerializer,
    ModeratorQuestionareUserAnswerAdminDetailSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class ModeratorQuestionareCategoryView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = CustomPagination

    def get_queryset(self):
        return QuestionnaireCategory.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorQuestionareCategorySerializer
        return ModeratorQuestionareCategoryDetailSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Category created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorQuestionareCategoryDetailView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ModeratorQuestionareCategoryDetailSerializer

    def get(self, request, pk):
        category = get_object_or_404(QuestionnaireCategory, pk=pk)
        serializer = self.serializer_class(category)
        return Response(
            {
                "success": True,
                "message": "Category detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        category = get_object_or_404(QuestionnaireCategory, pk=pk)
        serializer = self.serializer_class(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Category updated",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )

    def delete(self, request, pk):
        category = get_object_or_404(QuestionnaireCategory, pk=pk)
        category.delete()
        return Response({"success": True, "message": "Category deleted"})


######################################################################################


class ModeratorQuestionareView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = CustomPagination

    def get_queryset(self):
        return Questionnaire.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorQuestionareSerializer
        return ModeratorQuestionareCreateSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
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


class ModeratorQuestionareDetailView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ModeratorQuestionnaireDetailSerializer

    def get(self, request, pk):
        questionnaire = get_object_or_404(Questionnaire, pk=pk)
        serializer = self.serializer_class(questionnaire)
        return Response(
            {
                "success": True,
                "message": "Question detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        questionnaire = get_object_or_404(Questionnaire, pk=pk)
        serializer = self.serializer_class(
            questionnaire, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Question updated",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )

    def delete(self, request, pk):
        questionnaire = get_object_or_404(Questionnaire, pk=pk)
        questionnaire.delete()
        return Response({"success": True, "message": "Question deleted"})


########################################################################################


class ModeratorQuestionareUserAnswerView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = CustomPagination
    serializer_class = ModeratorQuestionareUserAnswerSerializer

    def get_queryset(self):
        return QuestionnaireUserAnswer.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ModeratorQuestionareUserDetailAnswerView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ModeratorQuestionareUserAnswerAdminDetailSerializer

    def get(self, request, pk):
        user_answer = get_object_or_404(QuestionnaireUserAnswer, pk=pk)
        serializer = self.serializer_class(user_answer)
        return Response(
            {
                "success": True,
                "message": "User answer detail",
                "data": serializer.data,
            }
        )
