from rest_framework import serializers

from apps.mobile.models.faq import FAQ


class ModeratorFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            "id",
            "question",
            "answer",
            "created_at",
        )


class ModeratorFAQDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            "id",
            "question_uz",
            "question_ru",
            "question_en",
            "answer_uz",
            "answer_ru",
            "answer_en",
            "created_at",
        )
