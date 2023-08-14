from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from .permissions import ProjectPermission, IssuePermission, CommentPermission
from contributors.models import Contributor

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IssuePermission]

    def perform_create(self, serializer):
        # 1. Attribuer l'utilisateur courant en tant qu'auteur de l'issue
        author = self.request.user

        # 2. Vérifier si l'utilisateur assigné est un contributeur du projet concerné
        assignee_id = self.request.data.get('assignee_user_id', None)
        project_id = self.request.data.get('project_id')
        
        if assignee_id:
            is_contributor = Contributor.objects.filter(user_id=assignee_id, project_id=project_id).exists()
            
            if not is_contributor:
                raise PermissionDenied("L'utilisateur assigné doit être un contributeur du projet.")

        serializer.save(author_user_id=author)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user)