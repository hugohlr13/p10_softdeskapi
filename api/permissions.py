from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from api.models import Issue
from contributors.models import Contributor


class ProjectPermission(permissions.BasePermission):
    """Allow actions if the user is the author of the project."""

    def has_object_permission(self, request, view, obj):
        """Grant permission for safe methods if the user is the project author; deny otherwise."""
        if request.method in permissions.SAFE_METHODS:
            return obj.author_user_id == request.user

        return obj.author_user_id == request.user


class IssuePermission(permissions.BasePermission):
    """Manage issue permissions based on user's role and relationship to the issue."""

    def _is_contributor(self, user, project):
        """Check if a user is a contributor to a project."""
        return Contributor.objects.filter(
            user_id=user.id, project_id=project.id
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Print IDs for debugging
        assignee_id = obj.assignee_user_id.id if obj.assignee_user_id else "No assignee"
        print(
            f"User ID: {request.user.id}, Author ID: {obj.author_user_id.id}, Assignee ID: {assignee_id}"
        )

        """Grant read permissions if the user is a contributor or involved with the issue; restrict edits to authors and assignees."""
        if request.method in permissions.SAFE_METHODS:
            return (
                self._is_contributor(request.user, obj.project_id)
                or obj.author_user_id == request.user
                or obj.assignee_user_id == request.user
            )

        # Deny patch requests if the user is not a contributor.
        if request.method == "PATCH" and not self._is_contributor(
            request.user, obj.project_id
        ):
            raise PermissionDenied(
                "Vous n'avez pas la permission d'effectuer cette action."
            )

        # Authors and assignees of the issue can edit.
        if obj.author_user_id == request.user or obj.assignee_user_id == request.user:
            return True

        # For PATCH requests, restrict updates to the 'status' field only.
        if request.method == "PATCH":
            if set(request.data.keys()) - {"status"}:
                raise PermissionDenied(
                    "Vous n'êtes pas assigné ou auteur de la tâche'."
                )
            return True

        # If the user is neither author, assignee, nor contributor only modifying the 'status' field, they do not have permission.
        return False


class CommentPermission(permissions.BasePermission):
    """Manage comment permissions, allowing only authors to edit or delete their comments."""

    def _is_contributor(self, user, project):
        """Check if a user is a contributor to a project."""
        return Contributor.objects.filter(
            user_id=user.id, project_id=project.id
        ).exists()

    def has_object_permission(self, request, view, obj):
        """Grant permission to view comments if the user is a project contributor; only the author can edit or delete."""
        if request.method in permissions.SAFE_METHODS:
            return self._is_contributor(request.user, obj.issue_id.project_id)

        # Seul l'auteur peut modifier ou supprimer le commentaire
        if obj.author_user_id == request.user:
            return True

        return False

    def has_permission(self, request, view):
        """Ensure POST requests are made by contributors of the issue's project."""
        if request.method == "POST":
            issue_id = request.data.get("issue_id", None)
            try:
                issue = Issue.objects.get(id=issue_id)
            except Issue.DoesNotExist:
                raise PermissionDenied("Issue associée n'existe pas.")

            if not self._is_contributor(request.user, issue.project_id):
                raise PermissionDenied(
                    "Vous devez être un contributeur du projet pour commenter cette issue."
                )

        return True
