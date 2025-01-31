from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.test import TestQuestion, Test
from apps.mobile.serializers.test import QuestionSerializer, TestSerializer


class TestList(APIView):
    serializer_class = TestSerializer
    permission_classes = [AllowAny]

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
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def post(self, request):
        test = request.data.get("test")
        results_data = request.data.get("results")

        correct_count = 0
        incorrect_count = 0
        not_attempted_count = 0
        total_score = 0

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
            try:
                correct_answer = question.answers.get(is_correct=True)
            except question.answers.model.DoesNotExist:
                return Response(
                    {"success": False, "message": "Correct answer not found"}
                )

            answered_correctly = False
            for answer in answers:
                answer_id = answer.get("answer_id")
                if answer_id == correct_answer.id:
                    answered_correctly = True
                    total_score += correct_answer.ball
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
                    "correct_count": correct_count,
                    "incorrect_count": incorrect_count,
                    "not_attempted_count": not_attempted_count,
                    "total_score": total_score,
                },
            }
        )
