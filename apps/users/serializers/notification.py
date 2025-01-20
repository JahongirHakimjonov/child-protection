from rest_framework import serializers

from apps.users.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "user", "banner", "title", "message", "created_at", "is_read")
