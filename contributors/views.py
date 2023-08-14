from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Contributor
from api.models import Project
from .serializers import ContributorSerializer

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def perform_create(self, serializer):
        project = self.request.data.get('project_id')
        if Project.objects.get(id=project).author_user_id == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("Vous devez être l'auteur du projet pour ajouter des contributeurs.")