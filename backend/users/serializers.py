import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from users.models import Organization, OrganizationUser

User = get_user_model()


def create_user_org_relation(organizations_data, user_obj):
    instances = [
        OrganizationUser(user=user_obj, organization=x)
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


class OrganizaitonsUserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all()
    )

    class Meta:
        model = OrganizationUser
        fields = ("id",)


class CustomUserSerializer(UserSerializer):
    photo = serializers.SerializerMethodField("get_image_url", read_only=True)
    organizations = OrganizationsSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "first_name",
            "last_name",
            "photo",
            "organizations",
            "is_active",
        )

    def get_image_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None


class CustomUserCreateSerializer(UserCreateSerializer):
    photo = Base64ImageField(required=False, allow_null=True)
    organizations = serializers.SlugRelatedField(
        slug_field="id",
        queryset=Organization.objects.all(),
        many=True,
        required=False,
    )

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

    def validate(self, data):
        organizations = data.get("organizations")
        if organizations is not None and len(set(organizations)) != len(
            organizations
        ):
            raise serializers.ValidationError(
                {"errors": "Нельзя добавлять одинаковые организации"}
            )

        return data

    def update(self, instance, validated_data):
        if "organizations" not in self.initial_data:
            instance = super().update(instance, validated_data)
            return instance
        organizations_data = validated_data.pop("organizations")
        OrganizationUser.objects.filter(user=instance).delete()
        instance = super().update(instance, validated_data)
        create_user_org_relation(organizations_data, instance)
        return instance

    def create(self, validated_data):
        if "organizations" not in self.initial_data:
            user_obj = User.objects.create_user(**validated_data)
            return user_obj
        organizations_data = validated_data.pop("organizations")
        user_obj = User.objects.create_user(**validated_data)
        create_user_org_relation(organizations_data, user_obj)
        return user_obj
