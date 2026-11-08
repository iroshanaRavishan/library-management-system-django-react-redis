from django.core.cache import cache
from django.db import transaction, IntegrityError
from django.utils import timezone

from django.db.models import F

from books.models import Book
from borrowing.models import BorrowTransaction
from books.cache import invalidate_borrowing_caches
from dashboard.services import invalidate_dashboard_cache


def invalidate_after_borrowing(book_id):
    """
    Invalidate caches affected by borrowing or returning a book.
    """
    invalidate_borrowing_caches(book_id)

    # Invalidate the book detail cache.
    cache.delete(f"book:{book_id}")

    # Invalidate book search results.
    # Requires a django-redis backend.
    cache.delete_pattern("book_search:*")

    # Invalidate popular books statistics.
    cache.delete("popular_books")

    # Invalidate dashboard statistics.
    invalidate_dashboard_cache()


def borrow_book(user, book_id, due_date):
    """
    Handles the complete business process of borrowing a book.
    Uses conditional database updates to prevent negative availability.
    """

    try:
        with transaction.atomic():

            # Check whether the book exists.
            book_exists = Book.objects.filter(id=book_id).exists()

            if not book_exists:
                raise ValueError("Book not found.")

            # Prevent duplicate active borrowing.
            already_borrowed = BorrowTransaction.objects.filter(
                user=user,
                book_id=book_id,
                returned_at__isnull=True,
            ).exists()

            if already_borrowed:
                raise ValueError(
                    "You have already borrowed this book."
                )

            # Decrease available copies only if at least one copy exists.
            updated_rows = Book.objects.filter(
                id=book_id,
                available_copies__gt=0,
            ).update(
                available_copies=F("available_copies") - 1
            )

            if updated_rows == 0:
                raise ValueError(
                    "No copies of this book are currently available."
                )

            # Create the borrowing transaction.
            borrow_transaction = BorrowTransaction.objects.create(
                user=user,
                book_id=book_id
            )
=

    except IntegrityError:
        # The database-level unique constraint protects against
        # simultaneous duplicate borrowing requests.
        already_borrowed = BorrowTransaction.objects.filter(
            user=user,
            book_id=book_id,
            returned_at__isnull=True,
        ).exists()

        if already_borrowed:
            raise ValueError(
                "You have already borrowed this book."
            )

        raise


def return_book(transaction_id):
    """
    Handles the complete business process of returning a book.
    Prevents the same transaction from being returned twice.
    """

    with transaction.atomic():

        # Find the borrowing transaction.
        borrow_transaction = BorrowTransaction.objects.get(
            id=transaction_id
        )

        book_id = borrow_transaction.book_id

        # Update only if the transaction has not already been returned.
        updated_rows = BorrowTransaction.objects.filter(
            id=transaction_id,
            returned_at__isnull=True,
        ).update(
            returned_at=timezone.now()
        )

        if updated_rows == 0:
            raise ValueError(
                "This book has already been returned."
            )

        # Increase available copies only when below total copies.
        updated_books = Book.objects.filter(
            id=book_id,
            available_copies__lt=F("total_copies"),
        ).update(
            available_copies=F("available_copies") + 1
        )

        if updated_books == 0:
            raise ValueError(
                "Book availability is inconsistent. "
                "Please contact the librarian."
            )

        # Invalidate affected caches after successful commit.
        transaction.on_commit(
            lambda book_id=book_id:
                invalidate_after_borrowing(book_id)
        )

        # Refresh the object to include the updated return time.
        borrow_transaction.refresh_from_db()

        return borrow_transaction
        