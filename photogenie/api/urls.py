from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, UserPostViewSet, DownloadImageView

router = DefaultRouter()
router.register('user-posts', UserPostViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-posts/<int:pk>/download', DownloadImageView.as_view(), name='download-image'),
]
