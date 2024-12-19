from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from users.models import Organization

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related("organizations")


class OrganizationViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Organization.objects.all()
