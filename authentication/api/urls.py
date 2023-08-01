from django.urls import path

from .views import LoginAPIView, LogoutAPIView, SignupAPIView

urlpatterns = [
    path('api/login', LoginAPIView.as_view()),
    path('api/signup', SignupAPIView.as_view()),
    path('api/logout', LogoutAPIView.as_view()),
]

