from rest_framework import serializers

from apps.mobile.models.question import (
    Question,
    QuestionCategory,
)


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ["id", "name"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "category", "title", "description", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = QuestionCategorySerializer(instance.category).data
        return response
