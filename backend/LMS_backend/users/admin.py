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

    # Filters shown in the right sidebar of Django Admin.
    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    # Fields used when searching from the Django Admin search box.
    search_fields = (
        "username",
        "email",
        "full_name",
    )

    ordering = ("id",)
