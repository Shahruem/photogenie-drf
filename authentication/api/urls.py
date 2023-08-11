from django.urls import path
from rest_framework_simplejwt.views import (TokenBlacklistView,
                                            TokenObtainPairView)

from authentication.api.views import SignupAPIView

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('signup', SignupAPIView.as_view(), name='signup'),
    path('logout', TokenBlacklistView.as_view(), name='logout'),
]
