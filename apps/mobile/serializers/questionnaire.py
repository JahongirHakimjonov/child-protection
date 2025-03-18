from rest_framework import serializers

from apps.mobile.models.questionnaire import (
    Questionnaire,
    QuestionnaireAnswer,
    QuestionnaireCategory,
    QuestionnaireUserAnswer,
)


class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = (
            "id",
            "title",
            "description",
            "created_at",
        )


class QuestionnaireAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireAnswer
        fields = (
            "id",
            "answer",
            "created_at",
        )


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = (
            "id",
            "category",
            "question",
            "is_text_answer",
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["answers"] = QuestionnaireAnswerSerializer(
            instance.answers.all(), many=True
        ).data
        return data


class QuestionnaireUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireUserAnswer
        fields = (
            "id",
            "questionnaire",
            "answer",
            "answer_text",
            "created_at",
        )
