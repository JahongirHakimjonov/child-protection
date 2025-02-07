from rest_framework import serializers

from apps.mobile.models.news import News


class ModeratorNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "description",
            "banner",
            "view_count",
            "created_at",
        )


class ModeratorNewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "description_uz",
            "description_ru",
            "description_en",
            "banner",
            "view_count",
            "created_at",
        )
