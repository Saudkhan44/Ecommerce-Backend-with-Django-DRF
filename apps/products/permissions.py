from rest_framework.permissions import BasePermission


class IsManagerOrReadOnly(BasePermission):
    """
    Managers can create/update/delete products.
    Normal users can only read.
    """

    def has_permission(self, request, view):

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return request.user.is_authenticated and (request.user.role == "manager" or request.user.role == "admin")