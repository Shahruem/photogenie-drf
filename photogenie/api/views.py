from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet

from photogenie.models import Post, Category

from .serializers import PostSerializer, CreatePostSerializer, CategorySerializer
from .signals import increment_views_signal


class CategoryListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserPostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]

    class Meta:
        model = Post

    def retrieve(self, request, *args, **kwargs):
        increment_views_signal.send(sender=self.__class__, instance=self.get_object())
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['published_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'Post created successfully',
        })

    def update(self, request, *args, **kwargs):
        request.data['published_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'Post updated successfully',
        })

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            'message': 'Deleted successfully',
        })

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            serializer_class = CreatePostSerializer
        else:
            serializer_class = PostSerializer

        return serializer_class

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


class PostListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all().order_by('views')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['published_by__username', 'categories__name']
    search_fields = ['published_by__username', 'categories__name']






