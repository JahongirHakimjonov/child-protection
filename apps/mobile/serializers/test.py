from rest_framework import serializers

from apps.mobile.models.test import Answer, TestQuestion, Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "title",
            "description",
            "banner",
            "question_count",
        )


class TestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "answer",
            "type",
        )


class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "question",
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["answers"] = TestAnswerSerializer(
            instance.answers.all(), many=True
        ).data
        return response
