from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, UserPostViewSet, DownloadImageView

router = DefaultRouter()
router.register('photos', UserPostViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('photos/<int:pk>/download', DownloadImageView.as_view()),
]
