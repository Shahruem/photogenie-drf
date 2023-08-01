from rest_framework import serializers
from photo_management.models import Category, Photo
from authentication.api.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class PhotoSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    published_by = UserSerializer()

    class Meta:
        model = Photo
        fields = '__all__'

