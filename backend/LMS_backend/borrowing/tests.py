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
