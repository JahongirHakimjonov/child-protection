from rest_framework import serializers

from apps.users.models.notification import Notification


class ModeratorNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "user",
            "banner",
            "title",
            "message",
            "is_read",
            "type",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["id", "created_at", "updated_at"]


class ModeratorNotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "user",
            "banner",
            "title_uz",
            "title_ru",
            "title_en",
            "message_uz",
            "message_ru",
            "message_en",
            "is_read",
            "type",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "title": {"required": False},
            "title_uz": {"required": False},
            "title_ru": {"required": False},
            "title_en": {"required": False},
            "message": {"required": False},
            "message_uz": {"required": False},
            "message_ru": {"required": False},
            "message_en": {"required": False},
        }
