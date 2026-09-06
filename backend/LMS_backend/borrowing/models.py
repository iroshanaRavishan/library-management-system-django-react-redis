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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrow_transactions",
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrow_transactions",
    )

    borrowed_at = models.DateTimeField(
        auto_now_add=True
    )

    due_date = models.DateTimeField()

    returned_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-borrowed_at"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    @property
    def is_returned(self):
        """
        Returns True when the book has been returned.
        """
        return self.returned_at is not None

    @property
    def is_overdue(self):
        """
        Returns True when the book has not been returned
        and the due date has passed.
        """
        from django.utils import timezone

        return (
            self.returned_at is None
            and timezone.now() > self.due_date
        )