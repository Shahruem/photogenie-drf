from django.urls import path

from .views import PhotoListView

urlpatterns = [
    path('api/photos', PhotoListView.as_view()),
]