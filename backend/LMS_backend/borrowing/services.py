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
