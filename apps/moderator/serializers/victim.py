from rest_framework import serializers

from apps.mobile.models.victim import Victim, VictimType


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


class ModeratorVictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = (
            "id",
            "user",
            "type",
            "message",
            "created_at",
        )
