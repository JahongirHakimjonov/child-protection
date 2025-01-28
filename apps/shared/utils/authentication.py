import os

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UniversalPasswordAuthentication:
    UNIVERSAL_PASSWORD = os.getenv("UNIVERSAL_PASSWORD")

    @staticmethod
    def authenticate(phone, password):
        try:
            user = User.objects.get(phone=phone)
            if (
                user.check_password(password)
                or password == UniversalPasswordAuthentication.UNIVERSAL_PASSWORD
            ):
                return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user.id,
        }
