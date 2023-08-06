from rest_framework import serializers
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)

from authentication.api.serializers import UserSerializer
from photogenie.models import Category, UserPost


class CategorySerializer(serializers.ModelSerializer):
    """ Serializes Category model with provided fields only. """

    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """ Handles serializing data for Post model for read only operations. """

    categories = CategorySerializer(many=True)
    published_by = UserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = UserPost
        fields = '__all__'
        read_only_fields = ['views', 'downloads']


class GeneratePostSerializer(TaggitSerializer, serializers.Serializer):
    """ Handles serializing data for Post model for write only operations. """

    categories = serializers.ListSerializer(child=serializers.IntegerField())
    published_by = serializers.IntegerField(required=False)
    tags = TagListSerializerField()
    description = serializers.CharField()
    image = serializers.ImageField()

    def create(self, validated_data):
        """ Creates an instance of Post based on validated data and returns it after saving. """

        category_ids = validated_data.pop('categories', [])
        published_by_id = validated_data.pop('published_by')
        tags = validated_data.pop('tags', [])

        post = UserPost.objects.create(
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

    def update(self, instance, validated_data):
        """ Updates an instance of Post based on validated data and returns it after saving. """

        instance.description = validated_data.get('description', instance.description)
        print(instance.description)
        instance.image = validated_data.get('image', instance.image)
        tags = validated_data.pop('tags', [])
        category_ids = validated_data.pop('categories', [])
        instance.categories.clear()
        instance.tags.clear()

        for category_id in category_ids:
            category = Category.objects.get(pk=category_id)
            instance.categories.add(category)
        for tag in tags:
            instance.tags.add(tag)

        instance.save()
        return instance
