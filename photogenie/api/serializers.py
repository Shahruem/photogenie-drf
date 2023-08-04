from rest_framework import serializers
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)

from authentication.api.serializers import UserSerializer
from photogenie.models import Category, Post
from rest_framework.fields import CurrentUserDefault


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CreatePostSerializer(TaggitSerializer, serializers.ModelSerializer):
    categories = serializers.ListSerializer(child=serializers.IntegerField())
    published_by = serializers.IntegerField(required=False)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ['published_by', 'categories', 'tags', 'description', 'image']

    def create(self, validated_data):
        category_ids = validated_data.pop('categories', [])
        published_by_id = validated_data.pop('published_by')
        tags = validated_data.pop('tags', [])

        post = Post.objects.create(
            published_by_id=published_by_id,
            description=validated_data['description'],
            image=validated_data['image']
        )

        for category_id in category_ids:
            category = Category.objects.get(pk=category_id)
            post.categories.add(category)

        for tag in tags:
            post.tags.add(tag)

        return post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    published_by = UserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'



