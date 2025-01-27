from rest_framework import serializers

from apps.mobile.models.course import (
    CourseCategory,
    CourseLesson,
    CourseLessonResource,
)


class CourseCategorySerializer(serializers.ModelSerializer):
    progress_percent = serializers.SerializerMethodField()

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
            "progress_percent",
        ]

    def get_progress_percent(self, instance):
        if self.context.get("rq"):
            user = self.context["rq"].user
            if user.is_authenticated:
                viewed = instance.courses.filter(viewed__user=user).count()
                total = instance.courses.count()
                if total:
                    return round(viewed / total * 100, 2)
        return 0


class CourseLessonSerializer(serializers.ModelSerializer):
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
        response["category"] = CourseCategorySerializer(instance.category).data
        return response


class LessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonResource
        fields = ["id", "lesson", "title", "name", "file", "size", "type", "created_at"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["lesson"] = CourseLessonSerializer(instance.lesson).data
        return response
