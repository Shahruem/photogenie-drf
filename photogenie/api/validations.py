from authentication.api.validations import ValidationSerializer
from rest_framework import serializers
import re


class QueryValidationSerializer(ValidationSerializer):
    published_by = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    search = serializers.CharField(required=False)
    ordering = serializers.CharField(required=False)

    def validate(self, attrs):
        """
        Validates the query parameters with the checks that only search parameter is allowed if given
        or ordering should be specific and category should be of all lower-cased characters
        """

        search = attrs.get('search', None)
        published_by = attrs.get('published_by', None)
        category = attrs.get('category', None)
        ordering = attrs.get('ordering', None)
        allowed_orderings = ['views', 'downloads']

        if search and any([published_by, category, ordering]):
            raise serializers.ValidationError({'error': 'Either search is allowed or the other query parameters.'})
        if ordering and ordering not in allowed_orderings:
            raise serializers.ValidationError({'error': 'Ordering can only be according to views or downloads.'})
        if category and not re.match(r'^[a-z]*$', category):
            raise serializers.ValidationError({'error': 'Only lower-cased characters are allowed in category.'})

        return attrs
