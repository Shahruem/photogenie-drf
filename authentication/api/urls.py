from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import LogoutAPIView, SignupAPIView

urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('signup', SignupAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
]

