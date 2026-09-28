from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from borrowing.models import BorrowTransaction
from borrowing.serializers import (
    BorrowTransactionSerializer,
    BorrowBookSerializer,
    ReturnBookSerializer,
)
from borrowing.permissions import (
    IsLibrarian,
    IsOwnerOrLibrarian,
)
from borrowing.services import (
    borrow_book,
    return_book,
)


class BorrowBookView(APIView):
    """
    Allows an authenticated user to borrow a book.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Validate the request data.
        serializer = BorrowBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Call the business logic from services.py.
            transaction = borrow_book(
                user=request.user,
                book_id=serializer.validated_data["book_id"],
                due_date=serializer.validated_data["due_date"],
            )

        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert the created transaction into API response data.
        response_serializer = BorrowTransactionSerializer(
            transaction,
            context={"request": request},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ReturnBookView(APIView):
    """
    Allows an authenticated user to return a book.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Validate the request data.
        serializer = ReturnBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_id = serializer.validated_data["transaction_id"]

        try:
            # Find the transaction first so we can verify ownership.
            transaction = BorrowTransaction.objects.get(
                id=transaction_id
            )

        except BorrowTransaction.DoesNotExist:
            return Response(
                {"detail": "Borrowing transaction not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
