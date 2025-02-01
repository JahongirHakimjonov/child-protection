from rest_framework import serializers

from apps.mobile.models.course import (
    CourseCategory,
    CourseLesson,
    CourseLessonResource,
)


class ModeratorCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = [
            "id",
            "title",
            "sub_title",
            "description",
            "image",
            "lesson_count",
            "first_color",
            "second_color",
        ]


class ModeratorCourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = [
            "id",
            "category",
            "title",
            "description",
            "text",
            "image",
            "likes_count",
            "students_count",
            "audio_count",
            "video_count",
            "document_count",
            "test_count",
            "created_at",
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = ModeratorCourseCategorySerializer(instance.category).data
        return response


class ModeratorLessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonResource
        fields = [
            "id",
            "lesson",
            "title",
            "description",
            "banner",
            "name",
            "file",
            "size",
            "type",
            "created_at",
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["lesson"] = ModeratorCourseLessonSerializer(instance.lesson).data
        return response
