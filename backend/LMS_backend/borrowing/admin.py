from django.contrib import admin

from .models import BorrowTransaction


@admin.register(BorrowTransaction)
class BorrowTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "book"
    )