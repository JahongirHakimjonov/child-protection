from rest_framework import serializers

from apps.mobile.models.news import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "description",
            "banner",
            "created_at",
        )
