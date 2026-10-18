from datetime import datetime, time, timedelta

from django.core.cache import cache
from django.db.models import Count
from django.utils import timezone

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated


class DashboardView(APIView):
    """
    Returns library statistics, cached in Redis for five minutes.
    """

    permission_classes = [IsAuthenticated]
