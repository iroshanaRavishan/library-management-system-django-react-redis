from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    # Total number of book records in the library.
    total_books = serializers.IntegerField()

    # Total copies that are currently available.
    available_copies = serializers.IntegerField()

    # Total registered user accounts.
    total_members = serializers.IntegerField()

    # Number of transactions that have not been returned.
    currently_borrowed = serializers.IntegerField()

    # Transactions created today.
    borrowed_today = serializers.IntegerField()
