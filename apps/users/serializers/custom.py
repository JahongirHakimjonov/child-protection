from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User, ActiveSessions


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number_field = "phone"

    def validate(self, attrs):
        credentials = {
            "phone": attrs.get(self.phone_number_field),
            "password": attrs.get("password"),
        }

        user = User.objects.filter(phone=credentials["phone"]).first()
        if user:
            user = authenticate(phone=user.phone, password=credentials["password"])

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        token = super().get_token(user)

        token["phone"] = user.phone

        return {
            "refresh": str(token),
            "access": str(token.access_token),
            "user": user.id,
        }


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get("refresh")

        if refresh is None:
            raise serializers.ValidationError("No refresh token provided")

        return {"refresh": refresh}


class BlockSessionSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()


class ActiveSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveSessions
        fields = (
            "id",
            "user",
            "ip",
            "user_agent",
            "location",
            "last_activity",
        )
