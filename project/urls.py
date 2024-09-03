from django.urls import path

from api.v1.base import api as api_v1

urlpatterns = [
    path("api/v1/", api_v1.urls, name="api-v1"),
]
