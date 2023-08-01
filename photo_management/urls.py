from django.urls import include, path

urlpatterns = [
    path('', include('photo_management.api.urls')),
]
