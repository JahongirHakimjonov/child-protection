from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.test import Test, TestQuestion, Answer
from apps.moderator.serializers.test import (
    ModeratorTestSerializer,
    ModeratorTestQuestionSerializer,
    ModeratorTestAnswerSerializer,
    ModeratorTestDetailSerializer,
    ModeratorTestQuestionDetailSerializer,
    ModeratorTestAnswerDetailSerializer,
    ModeratorTestQuestionCreateSerializer,
)
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin


class ModeratorTestView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Test.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorTestSerializer
        return ModeratorTestDetailSerializer

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        lesson = request.query_params.get("lesson")
        queryset = self.get_queryset()

        tf = {"true": True, "false": False}
        if is_active is not None:
            queryset = queryset.filter(is_active=tf.get(is_active.lower(), None))

        if lesson:
            queryset = queryset.filter(lesson=lesson)

        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                        Q(title__icontains=search_term)
                        | Q(description__icontains=search_term)
                        | Q(question_count__icontains=search_term)
                        | Q(course__title__icontains=search_term)
                        | Q(course__description__icontains=search_term)
                        | Q(course__text__icontains=search_term)
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
                {"success": True, "message": "Test created", "data": serializer.data}
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorTestDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorTestDetailSerializer

    @extend_schema(
        operation_id="moderator_test_detail_get",
    )
    def get(self, request, pk):
        test = get_object_or_404(Test, pk)
        serializer = self.serializer_class(test)
        return Response(
            {
                "success": True,
                "message": "Test detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_test_detail_patch",
    )
    def patch(self, request, pk):
        test = get_object_or_404(Test, pk)
        serializer = self.serializer_class(test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Test updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "Test does not exist"})

    @extend_schema(
        operation_id="moderator_test_detail_delete",
    )
    def delete(self, request, pk):
        test = get_object_or_404(Test, pk)
        test.delete()
        return Response({"success": True, "message": "Test deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
class ModeratorTestQuestionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return TestQuestion.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorTestQuestionSerializer
        return ModeratorTestQuestionCreateSerializer

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        test = request.query_params.get("test")
        queryset = self.get_queryset()

        tf = {"true": True, "false": False}
        if is_active is not None:
            queryset = queryset.filter(is_active=tf.get(is_active.lower(), None))

        if test:
            queryset = queryset.filter(test=test)

        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                        Q(question__icontains=search_term)
                        | Q(test__title__icontains=search_term)
                        | Q(test__description__icontains=search_term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer_class()(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Test savollari muvaffaqiyatli yaratildi",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ModeratorTestQuestionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorTestQuestionDetailSerializer

    @extend_schema(
        operation_id="moderator_test_question_detail_get",
    )
    def get(self, request, pk):
        testquestion = get_object_or_404(TestQuestion, pk)
        serializer = self.serializer_class(testquestion)
        return Response(
            {
                "success": True,
                "message": "TestQuestion detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_test_question_detail_patch",
    )
    def patch(self, request, pk):
        testquestion = get_object_or_404(TestQuestion, pk)
        serializer = self.serializer_class(testquestion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "TestQuestion updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "TestQuestion does not exist"})

    @extend_schema(
        operation_id="moderator_test_question_detail_delete",
    )
    def delete(self, request, pk):
        testquestion = get_object_or_404(TestQuestion, pk)
        testquestion.delete()
        return Response({"success": True, "message": "TestQuestion deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class ModeratorAnswerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Answer.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ModeratorTestAnswerSerializer
        return ModeratorTestAnswerDetailSerializer

    def get(self, request):
        search = request.query_params.get("search")
        is_correct = request.query_params.get("is_correct")
        queryset = self.get_queryset()

        tf = {"true": True, "false": False}
        if is_correct is not None:
            queryset = queryset.filter(is_correct=tf.get(is_correct.lower(), None))

        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                        Q(question__question__icontains=search_term)
                        | Q(answer__icontains=search_term)
                        | Q(type__icontains=search_term)
                        | Q(ball__icontains=search_term)
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
                    "message": "Answer created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorAnswerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorTestAnswerDetailSerializer

    @extend_schema(
        operation_id="moderator_answer_detail_get",
    )
    def get(self, request, pk):
        answer = get_object_or_404(Answer, pk)
        serializer = self.serializer_class(answer)
        return Response(
            {
                "success": True,
                "message": "Answer detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_answer_detail_patch",
    )
    def patch(self, request, pk):
        answer = get_object_or_404(Answer, pk)
        serializer = self.serializer_class(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Answer updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "Answer does not exist"})

    @extend_schema(
        operation_id="moderator_answer_detail_delete",
    )
    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk)
        answer.delete()
        return Response({"success": True, "message": "Answer deleted"})
