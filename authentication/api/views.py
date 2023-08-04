from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView

from .serializers import SignupSerializer, UserSerializer


class SignupAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'Sign up successful',
        })


class LogoutAPIView(TokenBlacklistView):

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({'detail': 'Refresh token blacklisted.'}, status=status.HTTP_204_NO_CONTENT)


