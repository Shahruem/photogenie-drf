from django.http import FileResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from photogenie.models import Category, UserPost

from photogenie.api.serializers import (CategorySerializer, GeneratePostSerializer,
                                        PostSerializer)
from photogenie.api.documentation import get_user_posts_query_parameters
from photogenie.api.utils import filter_queryset


class CategoryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """ This viewset allows users to view the list of available categories and retrieve individual category details. """

    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserPostViewSet(GenericViewSet, ListModelMixin, DestroyModelMixin):
    """ This viewset handles CRUD and download operations for UserPost model. """

    queryset = UserPost.objects.select_related('published_by').prefetch_related('categories', 'tags')
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        manual_parameters=get_user_posts_query_parameters(),
        responses={200: PostSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """ Generates a paginated list of all Posts in JSON format. """

        search = self.request.query_params.get('search', None)
        published_by = self.request.query_params.get('published_by', None)
        category = self.request.query_params.get('category', None)
        ordering = self.request.query_params.get('ordering', None)
        self.queryset = filter_queryset(
            queryset=self.queryset,
            search=search,
            ordering=ordering,
            published_by=published_by,
            category=category
        )
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
        Updates  a Post with the given JSON formatted data.
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


class DownloadImageView(RetrieveAPIView):
    """ Retrieves the image to be downloaded of the requested post with ID and increases download count. """

    queryset = UserPost.objects.select_related('published_by').prefetch_related('categories', 'tags')
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        img = instance.image
        instance.downloads += 1
        instance.save()
        response = FileResponse(open(img.path, 'rb'), content_type='image/*')
        response['dimensions'] = instance.dimensions
        response['Content-Disposition'] = f'attachment; filename="{img.name}"'
        return response
