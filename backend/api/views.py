from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from users.models import Organization
from users.serializers import OrganizationsSerializer

User = get_user_model()


class OrganizationViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Organization.objects.all()
    serializer_class = OrganizationsSerializer
