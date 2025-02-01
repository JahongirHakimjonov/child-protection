from datetime import datetime

from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models.users import ActiveSessions
from apps.users.serializers.register import SocialAuthSerializer
from apps.users.services import RegisterService, Apple
from apps.users.services.google import Google


class SocialAuthView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    serializer_class = SocialAuthSerializer

    def post(self, request, provider_name, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get("code")
        id_token = serializer.validated_data.get("id_token")

        try:
            jwt_token = self.authenticate_with_provider(provider_name, code, id_token)
            self.create_active_session(request, jwt_token)
            return Response(
                {
                    "success": True,
                    "message": "Authentication successful",
                    "data": jwt_token,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError as e:
            return Response(
                {"success": False, "message": f"Missing key: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"An unexpected error occurred: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def authenticate_with_provider(self, provider_name, code, id_token=None):
        if provider_name == "google":
            return Google.authenticate(code)
        elif provider_name == "apple":
            return Apple.authenticate(code, id_token)
        else:
            raise ValueError("Unsupported provider")

    def create_active_session(self, request, jwt_token):
        ip_address = RegisterService.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown User Agent")
        location = RegisterService.get_location(ip_address)
        fcm_token = request.headers.get("FCM-Token")
        refresh_token_expiration = timezone.make_aware(
            datetime.fromtimestamp(
                RefreshToken(jwt_token.get("refresh")).payload["exp"]
            )
        )
        ActiveSessions.objects.create(
            user_id=jwt_token.get("user"),
            ip=ip_address,
            user_agent=user_agent,
            location=location,
            refresh_token=jwt_token.get("refresh"),
            access_token=jwt_token.get("access"),
            fcm_token=fcm_token if fcm_token else None,
            expired_at=refresh_token_expiration,
        )

    @staticmethod
    def get(request, provider_name, *args, **kwargs):
        try:
            url = SocialAuthView.get_auth_url(provider_name)
            return HttpResponseRedirect(url)
        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"success": False, "message": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def get_auth_url(provider_name):
        if provider_name == "google":
            return Google.get_auth_url()
        elif provider_name == "apple":
            return Apple.get_auth_url()
        else:
            raise ValueError("Unsupported provider")
