from django.db import transaction
from django.utils import timezone

def borrow_book(user, book_id, due_date):
    """
    Handles the complete business process of borrowing a book.
    """

    # Start a database transaction so all database changes
    # succeed together or are rolled back together.
    with transaction.atomic():

        # Get the book from the database.
        book = Book.objects.get(id=book_id)

        # Check whether the book has any available copies.
        if book.available_copies <= 0:
            raise ValueError("No copies of this book are currently available.")

        # Check whether this user already has an active borrowing
        # transaction for the same book.
        already_borrowed = BorrowTransaction.objects.filter(
            user=user,
            book=book,
            returned_at__isnull=True
        ).exists()

        # Prevent the same user from borrowing the same book twice
        # without returning the first copy.
        if already_borrowed:
            raise ValueError("You have already borrowed this book.")

        # Create the borrowing transaction.
        borrow_transaction = BorrowTransaction.objects.create(
            user=user,
            book=book,
            due_date=due_date
        )

        # Decrease the number of available copies by one.
        book.available_copies -= 1

        # Save the updated availability.
        book.save(update_fields=["available_copies"])

        # Invalidate caches because book availability has changed.
        cache.delete(f"book:{book.id}")
