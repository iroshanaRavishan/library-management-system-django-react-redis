from django.contrib import admin

from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Displays the Author model in the Django admin interface.
    list_display = (
        "id",
        "name",
    )

