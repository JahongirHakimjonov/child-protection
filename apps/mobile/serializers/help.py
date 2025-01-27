from rest_framework import serializers

from apps.mobile.models.help import Help


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ("id", "user", "longitude", "latitude", "message")
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"required": False},
            "longitude": {"required": True},
            "latitude": {"required": True},
            "message": {"required": False},
        }
