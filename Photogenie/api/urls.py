from django.urls import path

from .views import CreatePostView, PostListView, PostRetrieveView

urlpatterns = [
    path('photos', PostListView.as_view()),
    path('photos/upload', CreatePostView.as_view()),
    path('photos/<int:pk>', PostRetrieveView.as_view()),
]
