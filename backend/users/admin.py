from django.contrib import admin

from .models import User, Organization


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )
    search_fields = ("email",)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "description",
    )
