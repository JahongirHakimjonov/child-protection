from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.victim import Victim, VictimType
from apps.mobile.serializers.victim import VictimSerializer, VictimTypeSerializer


class VictimTypeList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VictimTypeSerializer

    def get_queryset(self):
        return VictimType.objects.filter(is_active=True)

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(
            {
                "success": True,
                "message": "Victim types fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class VictimList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VictimSerializer

    def get_queryset(self):
        return Victim.objects.filter(user=self.request.user)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Victims fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "success": True,
                    "message": "Victim created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "Invalid data",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
