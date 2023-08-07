from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Serializes User model to provide read only functionality. """

    class Meta:
        model = User
        fields = ['id', 'username']

    def run_validation(self, data=None):
        """
        Skips validation for the user instance because Model serializer only allows unique User each time it is
        called
        """
        pass


class SignupSerializer(serializers.ModelSerializer):
    """ Serializes User model to provide create functionality for user sign-up. """

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        """Validates data including password which uses Django's password validation. """

        try:
            validate_password(password=attrs['password'])
        except ValidationError as v:
            raise serializers.ValidationError({'password': v.messages})

        return attrs

    def create(self, validated_data):
        """ Creates and returns User based on validated data after saving it into database. """

        user = User.objects.create_user(**validated_data)
        user.save()
        return user
