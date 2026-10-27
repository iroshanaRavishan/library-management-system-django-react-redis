from datetime import datetime, time, timedelta

from django.core.cache import cache
from django.db.models import Count
from django.utils import timezone
from django.db.models import Count, Sum

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from borrowing.models import BorrowTransaction
from users.models import User

from dashboard.serializers import DashboardSerializer

from dashboard.cache_keys import (
    DASHBOARD_CACHE_KEY,
    DASHBOARD_CACHE_TIMEOUT,
)


class DashboardView(APIView):
    """
    Returns library statistics, cached in Redis for five minutes.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Return cached dashboard data when available.
        cached_data = cache.get(DASHBOARD_CACHE_KEY)

        if cached_data is not None:
            return Response(cached_data)

        # Use the current Django timezone.
        now = timezone.localtime()
        today_start = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        tomorrow_start = today_start + timedelta(days=1)

        # Count total books and available copies.
        book_statistics = Book.objects.aggregate(
            total_books=Count("id"),
            available_copies=Sum("available_copies"),
        )

        total_books = book_statistics["total_books"]
        available_copies = book_statistics["available_copies"] or 0

        # Count registered users.
        total_members = User.objects.count()

        # Count transactions that are still active.
        active_transactions = BorrowTransaction.objects.filter(
            returned_at__isnull=True
        )
        currently_borrowed = active_transactions.count()

        # Count transactions created today.
        borrowed_today = BorrowTransaction.objects.filter(
            borrowed_at__gte=today_start,
            borrowed_at__lt=tomorrow_start,
        ).count()

        # Count transactions returned today.
        returned_today = BorrowTransaction.objects.filter(
            returned_at__gte=today_start,
            returned_at__lt=tomorrow_start,
        ).count()

        # Count transactions that are overdue and not returned.
        overdue_transactions = active_transactions.filter(
            due_date__lt=timezone.now()
        ).count()

        # Calculate the five most borrowed books.
        popular_books_queryset = (
            Book.objects.annotate(
                borrow_count=Count("borrow_transactions")
            )
            .order_by("-borrow_count", "title")[:5]
        )

        popular_books = [
            {
                "id": book.id,
                "title": book.title,
                "borrow_count": book.borrow_count,
            }
            for book in popular_books_queryset
        ]

        # Build the dashboard response.
        data = {
            "total_books": total_books,
            "available_copies": available_copies,
            "total_members": total_members,
            "currently_borrowed": currently_borrowed,
            "borrowed_today": borrowed_today,
            "returned_today": returned_today,
            "overdue_transactions": overdue_transactions,
            "popular_books": popular_books,
        }

        # Validate the response structure.
        serializer = DashboardSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Cache the complete dashboard for five minutes.
        cache.set(
            DASHBOARD_CACHE_KEY,
            serializer.validated_data,
            timeout=DASHBOARD_CACHE_TIMEOUT,
        )

        return Response(serializer.validated_data)


