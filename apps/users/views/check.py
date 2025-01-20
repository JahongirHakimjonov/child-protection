from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import CheckPhoneSerializer

User = get_user_model()


class CheckPhoneView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CheckPhoneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["phone"]
        exists = User.objects.filter(email=email).exists()
        return Response({"success": not exists})
