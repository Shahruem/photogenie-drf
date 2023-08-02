from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

    def run_validation(self, data=None):
        pass


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        try:
            validate_password(password=attrs['password'])
        except ValidationError as v:
            raise serializers.ValidationError({'password': v.messages})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

