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

        # Search results may contain the old availability.
        keys = cache.keys("book_search:*")
        if keys:
            cache.delete_many(keys)

        # Dashboard statistics may also have changed.
        cache.delete("library_dashboard")

        # Popular books statistics may have changed.
        cache.delete("popular_books")

        # Return the newly created transaction.
        return borrow_transaction


def return_book(transaction_id):
    """
    Handles the complete business process of returning a book.
    """

    # Start a database transaction.
    with transaction.atomic():

        # Find the borrowing transaction.
        borrow_transaction = BorrowTransaction.objects.select_related(
            "book"
        ).get(id=transaction_id)

        # Make sure the book has not already been returned.
        if borrow_transaction.returned_at is not None:
            raise ValueError("This book has already been returned.")

        # Record the return time.
        borrow_transaction.returned_at = timezone.now()

        # Save the return time.
        borrow_transaction.save(update_fields=["returned_at"])

        # Get the related book.
        book = borrow_transaction.book

        # Increase the number of available copies by one.
        book.available_copies += 1

        # Save the updated availability.
        book.save(update_fields=["available_copies"])

        # Invalidate the book detail cache.
        cache.delete(f"book:{book.id}")

        # Invalidate book search caches.
        keys = cache.keys("book_search:*")
    