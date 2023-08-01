from rest_framework.generics import ListAPIView
from photo_management.models import Photo
from .serializers import PhotoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class PhotoListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

