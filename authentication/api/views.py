from rest_framework import generics
from rest_framework.permissions import AllowAny

from authentication.api.serializers import SignupSerializer


class SignupAPIView(generics.CreateAPIView):
    """ Signs up the user with provided data in JSON format. """

    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
