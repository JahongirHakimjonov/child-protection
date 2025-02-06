from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.serializers.help import HelpSerializer


class HelpView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HelpSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            user.sos_count += 1
            user.save()
            return Response(
                {
                    "status": "success",
                    "message": "Help request has been sent successfully to the admin.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "error",
                "message": "Help request could not be sent.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        queryset = request.user.help.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "status": "success",
                "message": "Help requests have been retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
