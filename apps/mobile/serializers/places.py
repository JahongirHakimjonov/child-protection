from rest_framework import serializers

from apps.mobile.models.places import Place


class PlaceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'name', 'longitude', 'latitude', 'distance', 'created_at']

    def get_distance(self, obj):
        return f"{obj.distance:.2f} KM" if hasattr(obj, 'distance') else None
