from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.models import Project

from .models import Contributor
from .serializers import ContributorSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all().order_by("id")
    serializer_class = ContributorSerializer

    def perform_create(self, serializer):
        project = self.request.data.get("project_id")
        if Project.objects.get(id=project).author_user_id == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                "Vous devez être l'auteur du projet pour ajouter des contributeurs."
            )

    def get_queryset(self):
        queryset = Contributor.objects.all().order_by("id")
        project_id = self.request.query_params.get("project_id", None)

        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset
