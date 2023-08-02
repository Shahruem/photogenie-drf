from rest_framework import serializers
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)

from authentication.api.serializers import UserSerializer
from photogenie.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    published_by = UserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'



