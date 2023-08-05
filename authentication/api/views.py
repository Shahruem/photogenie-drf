from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import SignupSerializer


class SignupAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
