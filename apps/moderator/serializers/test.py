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
    test = ModeratorTestSerializer()

    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "question",
            "is_active",
        )


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
