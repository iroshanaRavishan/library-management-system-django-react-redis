from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    # Total number of book records in the library.
    total_books = serializers.IntegerField()
