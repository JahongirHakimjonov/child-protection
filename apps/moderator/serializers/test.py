from rest_framework import serializers

from apps.mobile.models.test import Answer, TestQuestion, Test, AnswerType
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


class ModeratorQuestionSerializer(serializers.ModelSerializer):
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
        response["answers"] = ModeratorAnswerSerializer(
            instance.answers.all(), many=True
        ).data
        return response


class ModeratorAnswerSerializer(serializers.ModelSerializer):
    question = ModeratorQuestionSerializer()
    type = serializers.ChoiceField(choices=AnswerType)

    class Meta:
        model = Answer
        fields = (
            "id",
            "question",
            "answer",
            "type",
            "ball",
            "is_correct",
        )
