from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.test import TestQuestion, Test
from apps.mobile.serializers.test import TestQuestionSerializer, TestSerializer


class TestList(APIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="test",
        parameters=[
            OpenApiParameter(
                name="lesson_id", description="Filter", required=False, type=int
            ),
        ],
        responses={200: TestSerializer(many=True)},
    )
    def get(self, request, lesson_id=None):
        tests = Test.objects.filter(is_active=True, lesson_id=lesson_id)
        if not tests:
            return Response(
                {"success": False, "message": "Tests not found"}, status=404
            )
        serializer = self.serializer_class(tests, many=True)
        return Response(
            {"success": True, "message": "Tests list", "data": serializer.data}
        )


class TestQuestionList(APIView):
    serializer_class = TestQuestionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="question",
        parameters=[
            OpenApiParameter(
                name="test_id", description="Filter", required=True, type=int
            ),
        ],
        responses={200: TestQuestionSerializer(many=True)},
    )
    def get(self, request, test_id=None):
        questions = TestQuestion.objects.filter(is_active=True, test_id=test_id)
        if not questions:
            return Response(
                {"success": False, "message": "Questions not found"}, status=404
            )
        serializer = self.serializer_class(questions, many=True)
        return Response(
            {"success": True, "message": "Questions list", "data": serializer.data}
        )


class TestResult(APIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            test = request.data.get("test")
            results_data = request.data.get("results")
            if not results_data:
                return Response(
                    {"success": False, "message": "Results not found"}, status=400
                )

            correct_count = 0
            incorrect_count = 0
            not_attempted_count = 0
            total_score = 0
            question_count = len(results_data)

            for result in results_data:
                question_id = result.get("question_id")
                answers = result.get("answers")
                if not answers:
                    not_attempted_count += 1
                    continue

                try:
                    question = TestQuestion.objects.get(id=question_id)
                except TestQuestion.DoesNotExist:
                    return Response({"success": False, "message": "Question not found"})

                correct_answers = question.answers.filter(is_correct=True)
                if not correct_answers.exists():
                    return Response(
                        {"success": False, "message": "Correct answer not found"}
                    )

                answered_correctly = False
                for answer in answers:
                    answer_id = answer.get("answer_id")
                    if correct_answers.filter(id=answer_id).exists():
                        answered_correctly = True
                        total_score += correct_answers.first().ball
                        break

                if answered_correctly:
                    correct_count += 1
                else:
                    incorrect_count += 1

            return Response(
                {
                    "success": True,
                    "message": "Test result",
                    "data": {
                        "test": test,
                        "question_count": question_count,
                        "correct_count": correct_count,
                        "incorrect_count": incorrect_count,
                        "not_attempted_count": not_attempted_count,
                        "total_score": total_score,
                    },
                }
            )
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=500)
