from rest_framework import permissions


class IsLibrarianOrReadOnly(permissions.BasePermission):
    # Allows anyone who is authenticated to read data.
    # Only librarians can create, update, or delete data.

