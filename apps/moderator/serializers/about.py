from rest_framework import serializers

from apps.mobile.models.about import About, AboutProject


class ModeratorAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = (
            "id",
            "title",
            "description",
            "image",
            "full_name",
            "created_at",
        )


class ModeratorAboutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "description_uz",
            "description_ru",
            "description_en",
            "image",
            "full_name",
            "created_at",
        )


class ModeratorAboutProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutProject
        fields = (
            "id",
            "title",
            "description",
            "image",
            "created_at",
        )


class ModeratorAboutProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutProject
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "description_uz",
            "description_ru",
            "description_en",
            "image",
            "created_at",
        )
