from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models.users import User
from apps.moderator.serializers.user import ModeratorUserSerializer
from apps.shared.permissions.admin import IsAdmin


class ModeratorUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorUserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset, many=True)
        return Response(
            {"success": True, "message": "User list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "User created", "data": serializer.data}
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorUserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorUserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User does not exist"})

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = self.serializer_class(data=user)
        return Response(
            {
                "success": True,
                "message": "User detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "User updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "User does not exist"})

    def delete(self, request, pk):
        user = self.get_object(pk=pk)
        user.delete()
        return Response({"success": True, "message": "User deleted"})
