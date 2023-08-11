from authentication.api.validations import ValidationSerializer
from rest_framework import serializers
from re import match


class QueryValidationSerializer(ValidationSerializer):
    published_by = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    search = serializers.CharField(required=False)
    ordering = serializers.ChoiceField(choices=['views', 'downloads'], required=False)

    def validate(self, attrs):
        """
        Validates the query parameters with the checks that only search parameter is allowed if given
        or ordering should be specific and category should be of all lower-cased characters
        """

        search = attrs.get('search', None)
        published_by = attrs.get('published_by', None)
        category = attrs.get('category', None)
        ordering = attrs.get('ordering', None)

        if search and (published_by or category or ordering):
            raise serializers.ValidationError({'error': 'Either search is allowed or the other query parameters.'})
        if category:
            attrs['category'] = category.lower()

        return attrs
