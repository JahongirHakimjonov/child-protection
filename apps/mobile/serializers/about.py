from rest_framework import serializers

from apps.mobile.models.about import About, AboutProject


class AboutSerializer(serializers.ModelSerializer):
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


class AboutProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutProject
        fields = (
            "id",
            "title",
            "description",
            "image",
            "created_at",
        )
