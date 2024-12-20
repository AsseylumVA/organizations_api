from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import OrganizationViewSet

router = DefaultRouter()

router.register("organizations", OrganizationViewSet, basename="organizations")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
