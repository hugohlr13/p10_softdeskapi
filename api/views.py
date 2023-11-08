from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from contributors.models import Contributor

from .models import Comment, Issue, Project
from .permissions import CommentPermission, IssuePermission, ProjectPermission
from .serializers import CommentSerializer, IssueSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Project CRUD operations."""

    queryset = Project.objects.all().order_by("id")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def perform_create(self, serializer):
        """Save the project with the current user set as the author."""
        serializer.save(author_user_id=self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Issue CRUD operations."""

    queryset = Issue.objects.all().order_by("id")
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IssuePermission]

    def perform_create(self, serializer):
        """Save the issue with the current user as the author and validate the assignee and author."""
        author = self.request.user
        project_id = self.request.data.get("project_id")
        if not Contributor.objects.filter(user_id=author.id, project_id=project_id).exists():
            raise PermissionDenied("Seuls les contributeurs du projet peuvent créer des problèmes.")

        assignee_id = self.request.data.get("assignee_user_id", None)
        if assignee_id:
            is_contributor = Contributor.objects.filter(
                user_id=assignee_id, project_id=project_id
            ).exists()
            if not is_contributor:
                raise PermissionDenied(
                    "L'utilisateur assigné doit être un contributeur du projet."
                )

        serializer.save(author_user_id=author)

    def _is_contributor(self, user, project_id):
        """Helper method to check if a user is a contributor of a project."""
        return Contributor.objects.filter(
            user_id=user.id, project_id=project_id
        ).exists()

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Comment CRUD operations."""

    queryset = Comment.objects.all().order_by("id")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]

    def perform_create(self, serializer):
        """Save the comment with the current user set as the author."""
        serializer.save(author_user_id=self.request.user)
