from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostListView, CategoryListView, UserPostViewSet

user_post_router = DefaultRouter()
user_post_router.register('photos', UserPostViewSet)

urlpatterns = [
    path('categories', CategoryListView.as_view()),
    path('photos', PostListView.as_view()),
    # path('photos/upload', CreatePostView.as_view()),
    # path('photos/<int:pk>', PostRetrieveView.as_view()),
    path('', include(user_post_router.urls))
]
