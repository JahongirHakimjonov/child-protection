from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.test import Test, TestQuestion, Answer
from apps.moderator.serializers.test import (
    ModeratorTestSerializer,
    ModeratorQuestionSerializer,
    ModeratorAnswerSerializer,
)
from apps.shared.permissions.admin import IsAdmin


class ModeratorTestView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorTestSerializer

    def get_queryset(self):
        return Test.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset, many=True)
        return Response(
            {"success": True, "message": "Test list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
    serializer_class = ModeratorTestSerializer

    def get_object(self, pk):
        try:
            return Test.objects.get(pk=pk)
        except Test.DoesNotExist:
            return Response({"success": False, "message": "Test does not exist"})

    def get(self, request, pk):
        test = self.get_object(pk=pk)
        serializer = self.serializer_class(data=test)
        return Response(
            {
                "success": True,
                "message": "Test detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        test = self.get_object(pk=pk)
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

    def delete(self, request, pk):
        test = self.get_object(pk=pk)
        test.delete()
        return Response({"success": True, "message": "Test deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class ModeratorTestQuestionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorQuestionSerializer

    def get_queryset(self):
        return TestQuestion.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset, many=True)
        return Response(
            {"success": True, "message": "TestQuestion list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "TestQuestion created",
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorTestQuestionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorQuestionSerializer

    def get_object(self, pk):
        try:
            return TestQuestion.objects.get(pk=pk)
        except TestQuestion.DoesNotExist:
            return Response(
                {"success": False, "message": "TestQuestion does not exist"}
            )

    def get(self, request, pk):
        testquestion = self.get_object(pk=pk)
        serializer = self.serializer_class(data=testquestion)
        return Response(
            {
                "success": True,
                "message": "TestQuestion detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        testquestion = self.get_object(pk=pk)
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

    def delete(self, request, pk):
        testquestion = self.get_object(pk=pk)
        testquestion.delete()
        return Response({"success": True, "message": "TestQuestion deleted"})


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class ModeratorAnswerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorQuestionSerializer

    def get_queryset(self):
        return Answer.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset, many=True)
        return Response(
            {"success": True, "message": "Answer list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
    serializer_class = ModeratorAnswerSerializer

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            return Response({"success": False, "message": "Answer does not exist"})

    def get(self, request, pk):
        answer = self.get_object(pk=pk)
        serializer = self.serializer_class(data=answer)
        return Response(
            {
                "success": True,
                "message": "Answer detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        answer = self.get_object(pk=pk)
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

    def delete(self, request, pk):
        answer = self.get_object(pk=pk)
        answer.delete()
        return Response({"success": True, "message": "Answer deleted"})
