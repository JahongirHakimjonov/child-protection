from rest_framework import serializers

from apps.mobile.models.victim import Victim, VictimType, VictimStatus
from apps.moderator.serializers.user import ModeratorUserSerializer


class ModeratorVictimTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VictimType
        fields = (
            "id",
            "name",
            "created_at",
        )


class ModeratorVictimTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VictimType
        fields = (
            "id",
            "name_uz",
            "name_ru",
            "name_en",
            "created_at",
        )


class ModeratorVictimStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VictimStatus
        fields = (
            "id",
            "name",
            "is_pending",
            "created_at",
        )


class ModeratorVictimStatusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VictimStatus
        fields = (
            "id",
            "name_uz",
            "name_ru",
            "name_en",
            "is_pending",
            "created_at",
        )


class ModeratorVictimSerializer(serializers.ModelSerializer):
    user = ModeratorUserSerializer()
    type = ModeratorVictimTypeSerializer()

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = ModeratorVictimStatusSerializer(instance.status).data
        return data
