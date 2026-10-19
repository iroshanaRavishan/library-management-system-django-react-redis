from datetime import datetime, time, timedelta

from django.core.cache import cache
from django.db.models import Count
from django.utils import timezone

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from borrowing.models import BorrowTransaction
from users.models import User

from dashboard.serializers import DashboardSerializer


class DashboardView(APIView):
    """
    Returns library statistics, cached in Redis for five minutes.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Return cached dashboard data when available.
        cache_key = "library_dashboard"
        cached_data = cache.get(cache_key)