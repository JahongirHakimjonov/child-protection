from rest_framework import serializers

from apps.mobile.models.saved import Saved
from apps.mobile.serializers.course import CourseLessonSerializer


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = ["id", "lesson", "user"]
        extra_kwargs = {"user": {"read_only": True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        context = self.context
        response["course"] = CourseLessonSerializer(
            instance.lesson, context=context
        ).data
        return response
