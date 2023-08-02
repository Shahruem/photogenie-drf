from rest_framework import serializers


class ValidationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        raise NotImplemented

    def update(self, instance, validated_data):
        raise NotImplemented
