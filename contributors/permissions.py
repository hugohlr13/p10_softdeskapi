from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedToViewContributors(BasePermission):
    """
    Permission to check if a user is authenticated to view contributors.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
