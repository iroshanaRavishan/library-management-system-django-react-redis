from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    """
    Allows access only to librarians/staff users.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
            )
        )


class IsOwnerOrLibrarian(permissions.BasePermission):
    """
    Allows users to access their own borrowing transactions.
    Librarians can access all transactions.
    """

    def has_object_permission(self, request, view, obj):

        # Librarians can access any borrowing transaction.
        if request.user.is_staff or request.user.is_superuser:
            return True
