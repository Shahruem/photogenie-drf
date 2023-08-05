from django.urls import path
from rest_framework_simplejwt.views import (TokenBlacklistView,
                                            TokenObtainPairView)

from .views import SignupAPIView

urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('signup', SignupAPIView.as_view()),
    path('logout', TokenBlacklistView.as_view()),
]
