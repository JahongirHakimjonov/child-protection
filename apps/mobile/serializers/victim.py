from rest_framework import serializers

from apps.mobile.models.victim import Victim, VictimType


class VictimTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VictimType
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
            "created_at",
        )
