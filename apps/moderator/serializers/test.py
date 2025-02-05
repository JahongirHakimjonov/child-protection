from rest_framework import serializers

from apps.mobile.models.test import Answer, TestQuestion, Test
from apps.moderator.serializers.course import ModeratorCourseLessonSerializer


class ModeratorTestSerializer(serializers.ModelSerializer):
    lesson = ModeratorCourseLessonSerializer()

    class Meta:
        model = Test
        fields = (
            "id",
            "lesson",
            "title",
            "description",
            "banner",
            "question_count",
            "is_active",
        )


class ModeratorTestDetailSerializer(serializers.ModelSerializer):
    lesson = ModeratorCourseLessonSerializer()

    class Meta:
        model = Test
        fields = (
            "id",
            "lesson",
            "title_uz",
            "title_ru",
            "title_en",
            "description_uz",
            "description_ru",
            "description_en",
            "banner",
            "question_count",
            "is_active",
        )


class ModeratorTestQuestionSerializer(serializers.ModelSerializer):
    test = ModeratorTestSerializer()

    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "question",
            "is_active",
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["answers"] = ModeratorTestAnswerSerializer(
            instance.answers.all(), many=True
        ).data
        return response


class ModeratorTestQuestionDetailSerializer(serializers.ModelSerializer):
    test = ModeratorTestSerializer()

    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "question_uz",
            "question_ru",
            "question_en",
            "is_active",
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["answers"] = ModeratorTestAnswerSerializer(
            instance.answers.all(), many=True
        ).data
        return response


class ModeratorTestAnswerSerializer(serializers.ModelSerializer):
    question = ModeratorTestQuestionSerializer()

    class Meta:
        model = Answer
        fields = ("id", "question", "answer", "type", "ball", "is_correct")


class ModeratorTestAnswerDetailSerializer(serializers.ModelSerializer):
    question = ModeratorTestQuestionSerializer()

    class Meta:
        model = Answer
        fields = (
            "id",
            "question",
            "answer_uz",
            "answer_ru",
            "answer_en",
            "type",
            "ball",
            "is_correct",
        )
