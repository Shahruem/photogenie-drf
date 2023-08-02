from django.urls import include, path

urlpatterns = [
    path('api/v1/auth/', include('authentication.api.urls')),
]
