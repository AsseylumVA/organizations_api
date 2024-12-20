import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from users.models import Organization, OrganizationUser

User = get_user_model()


def create_user_org_relation(organizations_data, user_obj):
    instances = [
        OrganizationUser(user=user_obj, organization=x["id"])
        for x in organizations_data
    ]
    OrganizationUser.objects.bulk_create(instances)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class OrganizationsSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="email"
    )

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "description",
            "users",
        )


class CustomUserSerializer(UserSerializer):
    photo = serializers.SerializerMethodField("get_image_url", read_only=True)
    organizations = OrganizationsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "first_name",
            "last_name",
            "photo",
            "organizations",
        )

    def get_image_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None


class OrganizaitonsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ("id",)


class CustomUserCreateSerializer(UserCreateSerializer):
    photo = Base64ImageField(required=False, allow_null=True)
    organizations = OrganizaitonsUserSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "photo",
            "organizations",
        )

    def create(self, validated_data):
        if "organizations" not in self.initial_data:
            user_obj = User.objects.create(**validated_data)
            return user_obj

        organizations_data = validated_data.pop("organizations")
        user_obj = User.objects.create(**validated_data)
        create_user_org_relation(organizations_data, user_obj)

        return user_obj
