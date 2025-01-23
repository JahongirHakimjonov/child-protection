import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_phone(self, value):
        if not re.match(
            r"^(998)(90|91|50|92|93|94|95|96|97|98|99|33|88|77)[0-9]{7}$",
            value,
        ):
            raise serializers.ValidationError(_("Telefon raqami noto‘g‘ri"))

        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(_("Telefon raqami allaqachon mavjud"))

        return value


class ConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        if not re.match(
            r"^(998)(90|91|50|92|93|94|95|96|97|98|99|33|88|77)[0-9]{7}$",
            value,
        ):
            raise serializers.ValidationError(_("Telefon raqami noto‘g‘ri"))
        return value


class ResendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)


class SocialAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    id_token = serializers.CharField(required=False)

    def validate(self, attrs):
        code = attrs.get("code")
        if not code:
            raise serializers.ValidationError("Code is required")
        return attrs
