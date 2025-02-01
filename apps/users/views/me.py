from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models.users import User
from apps.users.serializers.me import MeSerializer


class MeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        serializer = self.get_serializer(user)
        return Response(
            {"success": True, "message": "User data", "data": serializer.data}
        )
