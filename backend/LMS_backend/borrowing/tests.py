from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from books.models import Author, Book, Category, Publisher
from borrowing.models import BorrowTransaction
from borrowing.services import borrow_book, return_book
from users.models import User


class BorrowingServiceTests(TestCase):

    def setUp(self):
        # Create a normal library member.
        self.user = User.objects.create_user(
            username="testmember",
            email="member@example.com",
            password="TestPassword123!",
            full_name="Test Member",
            role=User.Role.MEMBER,
        )

        # Create the related book records.
        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(name="Test Category")
        self.publisher = Publisher.objects.create(name="Test Publisher")

        # Create a book with two available copies.
        self.book = Book.objects.create(
            isbn="9780000000001",
            title="Test Book",
            author=self.author,
            category=self.category,
            publisher=self.publisher,
            publication_year=2025,
            total_copies=2,
            available_copies=2,
        )

        self.due_date = timezone.now() + timedelta(days=14)

    def test_borrow_available_book(self):
        with patch("borrowing.services.invalidate_after_borrowing"):
            with self.captureOnCommitCallbacks(execute=True):
                borrowing = borrow_book(
                    user=self.user,
                    book_id=self.book.id,
                    due_date=self.due_date,
                )

        self.book.refresh_from_db()

        self.assertIsInstance(borrowing, BorrowTransaction)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(self.book.available_copies, 1)
        self.assertIsNone(borrowing.returned_at)

    def test_cannot_borrow_when_no_copies_are_available(self):
        self.book.available_copies = 0
        self.book.save(update_fields=["available_copies"])

        with self.assertRaisesMessage(
            ValueError,
            "No copies of this book are currently available.",
        ):
            borrow_book(
                user=self.user,
                book_id=self.book.id,
                due_date=self.due_date,
            )

        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 0)
        self.assertEqual(BorrowTransaction.objects.count(), 0)

    def test_user_cannot_borrow_same_book_twice(self):
        with patch("borrowing.services.invalidate_after_borrowing"):
            with self.captureOnCommitCallbacks(execute=True):
                borrow_book(
                    user=self.user,
                    
                )

