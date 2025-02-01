from rest_framework import serializers

from apps.mobile.models.help import Help


class ModeratorHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ("id", "user", "longitude", "latitude", "status")
