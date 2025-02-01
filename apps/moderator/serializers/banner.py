from rest_framework import serializers

from apps.mobile.models.banner import Banner


class ModeratorBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = (
            "id",
            "image",
            "link",
            "is_active",
            "created_at",
        )
