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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["lesson"] = ModeratorCourseLessonSerializer(instance.lesson).data
        return data


class ModeratorTestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "question",
            "is_active",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["answers"] = ModeratorTestAnswerSerializer(
            instance.answers.all(), many=True
        ).data
        return data


class ModeratorTestAnswerDetailSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            "id": {"read_only": False},
        }


class ModeratorTestQuestionDetailSerializer(serializers.ModelSerializer):
    answers = ModeratorTestAnswerDetailSerializer(many=True)

    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "question_uz",
            "question_ru",
            "question_en",
            "is_active",
            "answers",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["answers"] = ModeratorTestAnswerDetailSerializer(
            list(instance.answers.all()), many=True
        ).data
        return data

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers", None)
        instance = super().update(instance, validated_data)

        if answers_data is not None:
            for answer_data in answers_data:
                answer_data.pop("question", None)
                answer_id = answer_data.get("id", None)
                if answer_id:
                    try:
                        answer_instance = Answer.objects.get(
                            id=answer_id, question=instance
                        )
                    except Answer.DoesNotExist:
                        continue
                    for attr, value in answer_data.items():
                        setattr(answer_instance, attr, value)
                    answer_instance.save()
                else:
                    Answer.objects.create(question=instance, **answer_data)

        return instance


class ModeratorAnswerCreateSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            "id": {"read_only": True},
            "question": {"required": False},
        }


class ModeratorTestQuestionCreateSerializer(serializers.ModelSerializer):
    answers = ModeratorAnswerCreateSerializer(many=True)
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())

    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "question_uz",
            "question_ru",
            "question_en",
            "is_active",
            "answers",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        test_question = TestQuestion.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=test_question, **answer_data)
        return test_question


class ModeratorTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "answer", "type", "ball", "is_correct")
