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
        