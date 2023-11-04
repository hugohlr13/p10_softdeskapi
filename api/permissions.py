from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from api.models import Issue
from contributors.models import Contributor


class ProjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.author_user_id == request.user

        return obj.author_user_id == request.user


class IssuePermission(permissions.BasePermission):
    def _is_contributor(self, user, project):
        """Vérifie si l'utilisateur est un contributeur du projet."""
        return Contributor.objects.filter(
            user_id=user.id, project_id=project.id
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Imprimer les IDs pour le débug
        assignee_id = obj.assignee_user_id.id if obj.assignee_user_id else "No assignee"
        print(
            f"User ID: {request.user.id}, Author ID: {obj.author_user_id.id}, Assignee ID: {assignee_id}"
        )

        # Si l'utilisateur est contributeur du projet, il peut voir les issues
        if request.method in permissions.SAFE_METHODS:
            return (
                self._is_contributor(request.user, obj.project_id)
                or obj.author_user_id == request.user
                or obj.assignee_user_id == request.user
            )

        # Si la méthode est PATCH et l'utilisateur n'est pas un contributeur
        if request.method == "PATCH" and not self._is_contributor(
            request.user, obj.project_id
        ):
            raise PermissionDenied(
                "Vous n'avez pas la permission d'effectuer cette action."
            )

        # Si l'utilisateur est l'auteur ou assigné de l'issue
        if obj.author_user_id == request.user or obj.assignee_user_id == request.user:
            return True

        # Si la méthode est PATCH
        if request.method == "PATCH":
            # S'ils essaient de modifier autre chose que le statut, refusez.
            if set(request.data.keys()) - {"status"}:
                raise PermissionDenied(
                    "Vous ne pouvez mettre à jour que le champ 'statut'."
                )
            return True

        # Si l'utilisateur n'est ni auteur, ni assigné, ni contributeur ayant uniquement modifié le champ 'statut',
        # alors il n'a pas la permission
        return False


class CommentPermission(permissions.BasePermission):
    def _is_contributor(self, user, project):
        """Vérifie si l'utilisateur est un contributeur du projet."""
        return Contributor.objects.filter(
            user_id=user.id, project_id=project.id
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Si l'utilisateur est contributeur du projet, il peut voir les commentaires
        if request.method in permissions.SAFE_METHODS:
            return self._is_contributor(request.user, obj.issue_id.project_id)

        # Seul l'auteur peut modifier ou supprimer le commentaire
        if obj.author_user_id == request.user:
            return True

        return False

    def has_permission(self, request, view):
        # Si la méthode est POST, vérifiez si l'utilisateur est un contributeur de l'issue associée
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
