from rest_framework import serializers

from apps.mobile.models.help import Help, HelpStatus


class HelpSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=HelpStatus, default=HelpStatus.DANGER)

    class Meta:
        model = Help
        fields = ("id", "user", "longitude", "latitude", "status")
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"required": False},
            "longitude": {"required": True},
            "latitude": {"required": True},
        }
