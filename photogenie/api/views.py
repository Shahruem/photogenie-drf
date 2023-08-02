from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from photogenie.models import Post

from .serializers import PostSerializer
from .signals import increment_views_signal


class PostListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['published_by__username', 'categories__name']
    search_fields = ['published_by__username', 'categories__name']


class PostRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        increment_views_signal.send(sender=self.__class__, instance=self.get_object())
        return super().retrieve(request, *args, **kwargs)


class CreatePostView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        request.data['published_by'] = {"username": request.user.username}
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'Post created successfully',
        })




