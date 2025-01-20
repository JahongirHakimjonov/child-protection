from rest_framework import serializers


class CheckPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()
