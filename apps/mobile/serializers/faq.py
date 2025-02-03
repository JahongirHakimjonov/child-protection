from rest_framework import serializers

from apps.mobile.models.faq import FAQ


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            "id",
            "question",
            "answer",
            "created_at",
        )
