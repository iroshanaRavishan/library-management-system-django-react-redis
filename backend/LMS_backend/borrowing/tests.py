from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from books.models import Author, Book, Category, Publisher
from borrowing.models import BorrowTransaction
from borrowing.services import borrow_book, return_book
from users.models import User

