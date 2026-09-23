from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from borrowing.serializers import (BorrowBookSerializer)



class BorrowBookView(APIView):
    """
    Allows an authenticated user to borrow a book.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Validate the request data.
        serializer = BorrowBookSerializer(data=request.data)