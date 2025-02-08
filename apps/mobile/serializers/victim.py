from rest_framework import serializers

from apps.mobile.models.victim import Victim, VictimType, VictimStatus


class VictimTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VictimType
        fields = (
            "id",
            "name",
            "created_at",
        )


class VictimStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VictimStatus
        fields = (
            "id",
            "name",
            "created_at",
        )


class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = (
            "id",
            "user",
            "type",
            "message",
            "answer",
            "status",
            "created_at",
        )
        read_only_fields = ("user", "status", "created_at")
        extra_kwargs = {
            "user": {"required": False},
        }
