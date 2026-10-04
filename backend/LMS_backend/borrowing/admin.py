from django.contrib import admin

from .models import BorrowTransaction


@admin.register(BorrowTransaction)
class BorrowTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "book",
        "borrowed_at",
        "due_date",
        "returned_at",
        "is_returned",
        "is_overdue",
    )