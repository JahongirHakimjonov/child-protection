import logging

from django.utils.translation import gettext as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models.users import ActiveSessions
from apps.users.serializers.users import (
    UpdateAvatarSerializer,
    UpdateUserSerializer,
    DeleteAccountSerializer,
    LogOutSerializer,
)

logger = logging.getLogger(__name__)


class UpdateAvatarView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateAvatarSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(request.user, serializer.validated_data)
        return Response(
            {
                "success": True,
                "message": _("Avatar successfully updated."),
                "data": self.serializer_class(updated_instance).data,
            }
        )


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.update(request.user, serializer.validated_data)
        return Response(
            {
                "success": True,
                "message": _("User information successfully updated."),
                "data": self.serializer_class(updated_instance).data,
            }
        )


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: OpenApiResponse(DeleteAccountSerializer)},
        summary=_("Delete user account."),
        description=_("Delete authenticated user account."),
    )
    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        if user.check_password(request.data["password"]):
            user.delete()
            logger.info(f"User {user.username} deleted their account.")
            return response.Response(
                data={"success": True, "message": _("Account successfully deleted.")},
                status=status.HTTP_200_OK,
            )
        logger.warning(
            f"User {user.username} provided incorrect password for account deletion."
        )
        return response.Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"success": False, "message": _("Incorrect password provided.")},
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: OpenApiResponse(LogOutSerializer)},
        summary=_("Logout user."),
        description=_("Logout authenticated user."),
    )
    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        session_id = request.data["session_id"]
        session = ActiveSessions.objects.filter(user=user, id=session_id).update(
            is_active=False
        )
        if not session:
            logger.warning(
                f"User {user.username} provided incorrect session id for logout."
            )
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"success": False, "message": _("Incorrect session id provided.")},
            )
        logger.info(f"User {user.username} logged out from session {session_id}.")
        return response.Response(
            data={"success": True, "message": _("User successfully logged out.")},
            status=status.HTTP_200_OK,
        )
