from django.db.models import Q
from rest_framework import status
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
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserPostViewSet(GenericViewSet, RetrieveModelMixin, DestroyModelMixin, ListModelMixin):
    queryset = UserPost.objects.all()
    authentication_classes = (JWTAuthentication,)

    def list(self, request, *args, **kwargs):
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
        instance = self.get_object()
        if instance.published_by != request.user:
            instance.views += 1
            instance.save()
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['published_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            serializer_class = GeneratePostSerializer
        else:
            serializer_class = PostSerializer

        return serializer_class

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]
