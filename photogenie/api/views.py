from django.db.models import Q
from django.http import FileResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from photogenie.models import Category, UserPost

from .serializers import (CategorySerializer, GeneratePostSerializer,
                          PostSerializer)


class CategoryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """ This viewset allows users to view the list of available categories and retrieve individual category details. """

    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        """ Generates a paginated list of all available categories in JSON format. """

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Retrieves a category based on ID provided in JSON format."""

        return super().retrieve(request, *args, **kwargs)


class UserPostViewSet(GenericViewSet, DestroyModelMixin, ListModelMixin):
    """ This viewset handles CRUD and download operations for UserPost model. """

    queryset = UserPost.objects.select_related('published_by').prefetch_related('categories', 'tags')
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Searches the post based on username or category provided.',
                required=False,
            ),
            openapi.Parameter(
                name='published_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filters the post based on username.',
                required=False,
            ),
            openapi.Parameter(
                name='category',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filters the post based on category name.',
                required=False,
            ),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Sorts posts in ascending order based on views or downloads as provided.',
                required=False,
            ),
        ],
        responses={200: PostSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """ Generates a paginated list of all Posts in JSON format. """

        search = self.request.query_params.get('search', None)
        published_by = self.request.query_params.get('published_by', None)
        category = self.request.query_params.get('category', None)
        ordering = self.request.query_params.get('ordering', None)
        if search:
            q_published_by = Q(published_by__username=search)
            q_category_name = Q(categories__name=search)
            self.queryset = self.queryset.filter(q_published_by | q_category_name)
            if ordering:
                self.queryset = self.queryset.order_by(ordering)
            return super().list(request, *args, **kwargs)

        if published_by:
            self.queryset = self.queryset.filter(published_by__username=published_by)
        if category:
            self.queryset = self.queryset.filter(categories__name=category)
        if ordering:
            self.queryset = self.queryset.order_by(ordering)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a Post in JSON format with given ID and increases the view count of the post if that post is not
        published by the logged-in user.
        """

        instance = self.get_object()
        if instance.published_by != request.user:
            instance.views += 1
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a Post with the given JSON formatted data.

        [AUTHENTICATION REQUIRED]
        """

        request.data['published_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Updated a Post with the given JSON formatted data.

        [AUTHENTICATION REQUIRED]
        """

        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes the Post with given ID only if it belongs to the logged-in user.

        [AUTHENTICATION REQUIRED]
        """

        instance = self.get_object()
        if instance.published_by.id == request.user.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        """ Retrieves the image to be downloaded of the requested post with ID and increases download count. """

        instance = self.get_object()
        img = instance.image
        instance.downloads += 1
        instance.save()
        response = FileResponse(open(img.path, 'rb'), content_type='image/*')
        response['dimensions'] = instance.dimensions
        response['Content-Disposition'] = f'attachment; filename="{img.name}"'
        return response

    def get_serializer_class(self):
        """ Returns appropriate serializer class of Post based on HTTP method requested. """

        if self.action == 'create' or self.action == 'update':
            serializer_class = GeneratePostSerializer
        else:
            serializer_class = PostSerializer

        return serializer_class

    def get_permissions(self):
        """  Instantiates and returns appropriate permission class(es) of based on HTTP method requested. """

        if self.action == 'create' or self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]
