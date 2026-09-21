from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    """
    Allows access only to librarians/staff users.
    """

    def has_permission(self, request, view):