from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser):

    username = models.CharField(
        blank=True,
        max_length=150,
    )
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to="users/photos/", default=None)
    phone_number = models.CharField(max_length=12, blank=True)
    organizations = models.ManyToManyField(Organization)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")
