from rest_framework import serializers

from apps.mobile.models.saved import Saved
from apps.mobile.serializers.course import CourseSerializer


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = ["id", "course", "user"]
        extra_kwargs = {"user": {"read_only": True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        context = self.context
        response["course"] = CourseSerializer(instance.course, context=context).data
        return response
