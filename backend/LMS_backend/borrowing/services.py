from django.db import transaction
from django.utils import timezone

def borrow_book(user, book_id, due_date):
    """
    Handles the complete business process of borrowing a book.
    """
