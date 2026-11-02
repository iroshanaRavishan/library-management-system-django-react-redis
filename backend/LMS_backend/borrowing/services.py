from django.core.cache import cache
from django.db import transaction, IntegrityError
from django.utils import timezone

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

    with transaction.atomic():

        # Get the book from the database.
        book = Book.objects.get(id=book_id)

        # Check whether the book has available copies.
        if book.available_copies <= 0:
            raise ValueError(
                "No copies of this book are currently available."
            )

        # Check whether the user already has an active borrowing.
        already_borrowed = BorrowTransaction.objects.filter(
            user=user,
            book=book,
            returned_at__isnull=True,
        ).exists()

        if already_borrowed:
            raise ValueError(
                "You have already borrowed this book."
            )

        # Create the borrowing transaction.
        borrow_transaction = BorrowTransaction.objects.create(
            user=user,
            book=book,
            due_date=due_date,
        )

        # Decrease available copies.
        book.available_copies -= 1
        book.save(update_fields=["available_copies"])

        # Invalidate affected caches after the transaction commits.
        transaction.on_commit(
            lambda book_id=book.id: invalidate_after_borrowing(book_id)
        )

        return borrow_transaction


def return_book(transaction_id):
    """
    Handles the complete business process of returning a book.
    """

    with transaction.atomic():

        # Find the borrowing transaction.
        borrow_transaction = (
            BorrowTransaction.objects
            .select_related("book")
            .get(id=transaction_id)
        )

        # Prevent returning the same book twice.
        if borrow_transaction.returned_at is not None:
            raise ValueError(
                "This book has already been returned."
            )

        # Record the return time.
        borrow_transaction.returned_at = timezone.now()
        borrow_transaction.save(update_fields=["returned_at"])

        # Get the related book.
        book = borrow_transaction.book

        # Increase available copies.
        book.available_copies += 1
        book.save(update_fields=["available_copies"])

        # Invalidate affected caches after the transaction commits.
        transaction.on_commit(
            lambda book_id=book.id: invalidate_after_borrowing(book_id)
        )

        return borrow_transaction
