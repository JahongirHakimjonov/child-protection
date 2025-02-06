from rest_framework import serializers

from apps.users.models.users import User


class ModeratorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "username",
            "avatar",
            "role",
            "register_type",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "sos_count",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "username": {"required": False},
        }
