from rest_framework import serializers


class ValidationSerializer(serializers.Serializer):
    """ Provides abstract class for validation purposes. """

    def create(self, validated_data):
        raise NotImplemented

    def update(self, instance, validated_data):
        raise NotImplemented
