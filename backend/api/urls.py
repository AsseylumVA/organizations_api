from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import OrganizationViewSet, UserViewSet

router = DefaultRouter()

router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
