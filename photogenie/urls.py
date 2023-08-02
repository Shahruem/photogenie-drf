from django.urls import include, path

urlpatterns = [
    path('api/v1/photogenie/', include('photogenie.api.urls')),
]
