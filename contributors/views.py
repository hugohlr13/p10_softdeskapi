from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.models import Project

from .models import Contributor
from .serializers import ContributorSerializer
from .permissions import IsAuthenticatedToViewContributors


class ContributorViewSet(viewsets.ModelViewSet):
    """Viewset for handling Contributor operations."""

    queryset = Contributor.objects.all().order_by("id")
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticatedToViewContributors]

    def perform_create(self, serializer):
        """Create a Contributor, ensuring the requesting user is the project author."""
        project = self.request.data.get("project_id")
        if Project.objects.get(id=project).author_user_id == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                "Vous devez être l'auteur du projet pour ajouter des contributeurs."
            )

    def get_queryset(self):
        """Retrieve the queryset of Contributors, possibly filtered by project_id."""
        queryset = Contributor.objects.all().order_by("id")
        project_id = self.request.query_params.get("project_id", None)

        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset
