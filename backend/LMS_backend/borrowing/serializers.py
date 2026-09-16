from rest_framework import serializers

from borrowing.models import BorrowTransaction
from books.models import Book
from users.models import User


class BorrowTransactionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer used to display borrowing transaction information.
    """

    # User is displayed as a hyperlink to the user's detail endpoint.
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="user-detail"
    )

    # Book is displayed as a hyperlink to the book's detail endpoint.
    book = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="book-detail"
    )

    # These fields are calculated by the model.
    is_returned = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()