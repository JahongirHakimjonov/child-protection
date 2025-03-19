from rest_framework import serializers

from apps.mobile.models.questionnaire import (
    Questionnaire,
    QuestionnaireCategory,
    QuestionnaireUserAnswer,
    QuestionnaireAnswer,
    QuestionnaireUserAnswerDetail,
)
from apps.users.serializers.me import UserSerializer


class ModeratorQuestionareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = (
            "id",
            "title",
            "description",
            "is_active",
            "created_at",
        )


class ModeratorQuestionareCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "description_uz",
            "description_ru",
            "description_en",
            "is_active",
            "created_at",
        )


class ModeratorQuestionareAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireAnswer
        fields = (
            "id",
            "questionnaire",
            "answer",
            "is_active",
            "created_at",
        )


class ModeratorQuestionareAnswerAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireAnswer
        fields = (
            "id",
            "answer",
        )


class ModeratorQuestionareAnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireAnswer
        fields = (
            "id",
            "questionnaire",
            "answer_uz",
            "answer_ru",
            "answer_en",
            "is_active",
            "created_at",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "questionnaire": {"required": False},
        }


class ModeratorQuestionareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = (
            "id",
            "category",
            "question",
            "is_text_answer",
            "is_active",
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = ModeratorQuestionareCategorySerializer(
            instance.category
        ).data
        return data


class ModeratorQuestionareAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = (
            "id",
            "question",
        )


class ModeratorQuestionareCreateSerializer(serializers.ModelSerializer):
    answers = ModeratorQuestionareAnswerDetailSerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=QuestionnaireCategory.objects.filter(is_active=True)
    )

    class Meta:
        model = Questionnaire
        fields = (
            "id",
            "category",
            "question_uz",
            "question_ru",
            "question_en",
            "is_text_answer",
            "is_active",
            "created_at",
            "answers",
        )

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        questionnaire_question = Questionnaire.objects.create(**validated_data)
        for answer_data in answers_data:
            QuestionnaireAnswer.objects.create(
                questionnaire=questionnaire_question, **answer_data
            )
        return questionnaire_question


class ModeratorQuestionnaireDetailSerializer(serializers.ModelSerializer):
    answers = ModeratorQuestionareAnswerDetailSerializer(many=True)

    class Meta:
        model = Questionnaire
        fields = (
            "id",
            "category",
            "question_uz",
            "question_ru",
            "question_en",
            "is_text_answer",
            "is_active",
            "created_at",
            "answers",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["answers"] = ModeratorQuestionareAnswerDetailSerializer(
            list(instance.answers.all()), many=True
        ).data
        data["category"] = ModeratorQuestionareCategorySerializer(
            instance.category
        ).data
        return data

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers", None)
        instance = super().update(instance, validated_data)

        if answers_data is not None:
            for answer_data in answers_data:
                answer_data.pop("questionnaire", None)
                answer_id = answer_data.get("id", None)
                if answer_id:
                    try:
                        answer_instance = QuestionnaireAnswer.objects.get(
                            id=answer_id, questionnaire=instance
                        )
                    except QuestionnaireAnswer.DoesNotExist:
                        continue
                    for attr, value in answer_data.items():
                        setattr(answer_instance, attr, value)
                    answer_instance.save()
                else:
                    QuestionnaireAnswer.objects.create(
                        questionnaire=instance, **answer_data
                    )

        return instance


class ModeratorQuestionareUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireUserAnswer
        fields = (
            "id",
            "user",
            "category",
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserSerializer(instance.user).data
        data["category"] = ModeratorQuestionareCategorySerializer(
            instance.category
        ).data
        return data


class ModeratorQuestionareUserAnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireUserAnswerDetail
        fields = (
            "id",
            "questionnaire",
            "answer",
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["questionnaire"] = ModeratorQuestionareAddSerializer(
            instance.questionnaire
        ).data
        data["answer"] = ModeratorQuestionareAnswerAddSerializer(instance.answer).data
        return data


class ModeratorQuestionareUserAnswerAdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireUserAnswer
        fields = (
            "id",
            "user",
            "category",
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserSerializer(instance.user).data
        data["category"] = ModeratorQuestionareCategorySerializer(
            instance.category
        ).data
        data["answers"] = ModeratorQuestionareUserAnswerDetailSerializer(
            instance.user_answer_details.all(), many=True
        ).data
        return data
