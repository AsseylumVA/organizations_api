from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )
    search_fields = ("email",)
