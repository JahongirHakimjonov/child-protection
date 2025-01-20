from datetime import datetime

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import ActiveSessions
from apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    BlockSessionSerializer,
    ActiveSessionsSerializer,
)
from apps.users.serializers import CustomTokenRefreshSerializer
from apps.users.services import RegisterService


from django.utils import timezone


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jwt_token = serializer.validated_data
        ip_address = RegisterService.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown User Agent")
        location = RegisterService.get_location(ip_address)
        refresh_token = jwt_token.get("refresh")
        access_token = jwt_token.get("access")
        user_id = jwt_token.get("user")
        fcm_token = request.headers.get("FCM-Token")

        refresh_token_expiration = timezone.make_aware(
            datetime.fromtimestamp(RefreshToken(refresh_token).payload["exp"])
        )

        ActiveSessions.objects.create(
            user_id=user_id,
            ip=ip_address,
            user_agent=user_agent,
            location=location,
            refresh_token=refresh_token,
            access_token=access_token,
            fcm_token=fcm_token if fcm_token else None,
            expired_at=refresh_token_expiration,
        )

        return Response(
            {
                "success": True,
                "message": "Successfully logged in",
                "data": {"access": access_token, "refresh": refresh_token},
            },
            status=status.HTTP_200_OK,
        )


class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            user_id = token["user_id"]

            session = ActiveSessions.objects.filter(
                user_id=user_id, refresh_token=refresh_token, is_active=True
            ).first()
            if not session:
                return Response(
                    {"success": False, "message": "Invalid refresh token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_access_token = str(token.access_token)
            new_refresh_token = str(token)
            refresh_token_expiration = datetime.fromtimestamp(token.payload["exp"])

            session.access_token = new_access_token
            session.refresh_token = new_refresh_token
            session.expired_at = refresh_token_expiration
            session.save()

            return Response(
                {
                    "success": True,
                    "message": "Successfully refreshed",
                    "data": {
                        "access": new_access_token,
                        "refresh": new_refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BlockSessionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlockSessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data["session_id"]

        try:
            session = ActiveSessions.objects.get(id=session_id, user=request.user)
            session.is_active = False
            session.access_token = ""
            session.refresh_token = ""
            session.save()

            return Response(
                {"success": True, "message": "Session blocked successfully"},
                status=status.HTTP_200_OK,
            )
        except ActiveSessions.DoesNotExist:
            return Response(
                {"success": False, "message": "Session not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListSessionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveSessionsSerializer

    def get(self, request, *args, **kwargs):
        sessions = ActiveSessions.objects.filter(user=request.user, is_active=True)
        serializer = self.serializer_class(sessions, many=True)
        return Response(
            {
                "success": True,
                "message": "Successfully fetched",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
