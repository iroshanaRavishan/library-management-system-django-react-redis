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

    class Meta:
        model = BorrowTransaction

        fields = [
            "url",
            "id",
            "user",
            "book",
            "borrowed_at",
            "due_date",
            "returned_at",
            "is_returned",
            "is_overdue",
        ]

        extra_kwargs = {
            "url": {
                "view_name": "borrowing-detail"
            },
            "borrowed_at": {
                "read_only": True
            },
            "returned_at": {
                "read_only": True
            },
        }


class BorrowBookSerializer(serializers.Serializer):
    """
    Serializer used when a user wants to borrow a book.
    """

    # ID of the book the user wants to borrow.
    book_id = serializers.IntegerField()

    # Due date provided by the user.
    due_date = serializers.DateTimeField()

    def validate_book_id(self, value):
        """
        Make sure the requested book exists.
        """

        if not Book.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "The requested book does not exist."
            )

        return value

    def validate_due_date(self, value):
        """
        Make sure the due date is in the future.
        """

        from django.utils import timezone

        if value <= timezone.now():
            raise serializers.ValidationError(
                "Due date must be in the future."
            )

        return value


class ReturnBookSerializer(serializers.Serializer):
    """
    Serializer used when a user wants to return a book.
    """