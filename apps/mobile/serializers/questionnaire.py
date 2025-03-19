from django.utils import timezone
from rest_framework import serializers

from apps.mobile.models.questionnaire import (
    Questionnaire,
    QuestionnaireAnswer,
    QuestionnaireCategory,
    QuestionnaireUserAnswerDetail,
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
        model = QuestionnaireUserAnswerDetail
        fields = (
            "id",
            "questionnaire",
            "answer",
            "answer_text",
            "created_at",
        )

    def create(self, validated_data):
        user = self.context["rq"].user
        instance, created = QuestionnaireUserAnswerDetail.objects.update_or_create(
            user_answer__user=user,
            user_answer=validated_data["user_answer"],
            questionnaire=validated_data["questionnaire"],
            answer=validated_data["answer"],
            created_at__date=timezone.now().date(),
            defaults=validated_data,
        )
        return instance
