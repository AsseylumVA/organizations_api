from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Organization
from users.serializers import (
    OrganizationsSerializer,
    CustomUserSerializer,
    CustomUserCreateSerializer,
)
from users.permissions import IsAuthenticatedOrReadOnlyNotMe

User = get_user_model()


class OrganizationViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Organization.objects.all()
    serializer_class = OrganizationsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = (
        "get",
        "post",
        "patch",
    )
    permission_classes = (IsAuthenticatedOrReadOnlyNotMe,)

    def get_serializer_class(self):
        if self.action == "list":
            return CustomUserSerializer
        return CustomUserCreateSerializer

    @action(
        detail=False,
        methods=[
            "get",
            "patch",
        ],
    )
    def me(self, request):
        me_user = request.user
        if request.method == "PATCH":
            serializer = CustomUserCreateSerializer(
                me_user,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(me_user)
        return Response(serializer.data)
