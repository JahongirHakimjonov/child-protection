from rest_framework import serializers

from apps.mobile.models.course import (
    CourseCategory,
    Course,
    CourseLesson,
    CourseLessonResource,
)


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ["id", "name", "image"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "category",
            "image",
            "description",
            "lesson_count",
            "students_count",
            "saved_count",
            "is_active",
            "created_at",
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = CourseCategorySerializer(instance.category).data
        return response


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ["id", "course", "sort_number", "title", "description", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["resources"] = CourseLessonResourceSerializer(
            instance.resources, many=True
        ).data
        return response


class CourseLessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonResource
        fields = ["id", "lesson", "title", "file", "size", "type", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["lesson"] = CourseLessonSerializer(instance.lesson).data
        return response
