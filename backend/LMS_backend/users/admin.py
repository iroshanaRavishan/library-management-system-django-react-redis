from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Customize how the User model appears in Django Admin

    # Columns displayed in the Django Admin user list.
    list_display = (
        "id",
        "username",
        "email",
        "full_name",
        "role",
        "is_staff",
        "is_active",
    )

    ordering = ("id",)
