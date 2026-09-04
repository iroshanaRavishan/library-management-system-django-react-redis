from django.db import models
from django.conf import settings

from books.models import Book


class BorrowTransaction(models.Model):
    """
    Represents a book borrowing transaction.

    A transaction is created when a member borrows a book.
    When the book is returned, returned_at is populated.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL
    )