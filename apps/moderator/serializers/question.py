from rest_framework import serializers

from apps.mobile.models.question import (
    Question,
    QuestionCategory,
)


class ModeratorQuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ["id", "name", "image", "created_at"]


class ModeratorQuestionCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ["id", "name_uz", "name_ru", "name_en", "image", "created_at"]


class ModeratorQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "category", "title", "description", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = ModeratorQuestionCategorySerializer(
            instance.category
        ).data
        return response


class ModeratorQuestionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "category",
            "title_uz",
            "title_ru",
            "title_en",
            "description_uz",
            "description_ru",
            "description_en",
            "created_at",
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = ModeratorQuestionCategorySerializer(
            instance.category
        ).data
        return response
