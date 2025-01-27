from rest_framework import serializers

from apps.mobile.models.banner import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("id", "image", "link", "created_at")
