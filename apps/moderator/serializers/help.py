from rest_framework import serializers

from apps.mobile.models.help import Help
from apps.moderator.serializers.user import ModeratorUserSerializer


class ModeratorHelpSerializer(serializers.ModelSerializer):
    user = ModeratorUserSerializer()

    class Meta:
        model = Help
        fields = ("id", "user", "longitude", "latitude", "status", "created_at", "updated_at")
