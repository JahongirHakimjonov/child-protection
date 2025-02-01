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
