from rest_framework import serializers

from borrowing.models import BorrowTransaction
from books.models import Book
from users.models import User


class BorrowTransactionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer used to display borrowing transaction information.
    """
