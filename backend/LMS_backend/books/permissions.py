from rest_framework import permissions


class IsLibrarianOrReadOnly(permissions.BasePermission):
    # Allows anyone who is authenticated to read data.
    # Only librarians can create, update, or delete data.


    def has_permission(self, request, view):

        # GET, HEAD and OPTIONS are read-only operations.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only authenticated librarians can modify data.
        return (
            request.user.is_authenticated
            and request.user.role == "LIBRARIAN"
        )