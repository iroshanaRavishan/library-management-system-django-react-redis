from django.contrib import admin

from .models import Author, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Displays the Author model in the Django admin interface.
    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Displays the Category model in the Django admin interface.

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    # Displays the Publisher model in the Django admin interface.

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Displays the Book model in the Django admin interface.

    list_display = (
        "id",
        "title",
        "author",
        "category",
        "publisher",
    )

    list_filter = (
        "category",
        "publisher",
    )

    search_fields = (
        "title",
        "isbn",
    )