from rest_framework import serializers

from apps.mobile.models.places import Place


class ModeratorPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "name", "longitude", "latitude", "is_active", "created_at"]


class ModeratorPlaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "name_en",
            "longitude",
            "latitude",
            "is_active",
            "created_at",
        ]
