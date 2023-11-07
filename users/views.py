from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing user instances."""
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """ Create a User instance after validating the age. Users under 16 cannot register."""
        serializer = self.get_serializer(data=request.data)  # Gets the serializer
        serializer.is_valid(raise_exception=True)  # Checks if the data is valid

        age = serializer.validated_data.get("age")
        if age is not None and int(age) < 16:
            return Response(
                {"error": "Un utilisateur de moins de 16 ans ne peut pas s'inscrire."},
                status=400,
            )
        user = User(
            username=serializer.validated_data.get("username"),
            email=serializer.validated_data.get("email"),
            age=age,
            can_be_contacted=serializer.validated_data.get("can_be_contacted", False),
            can_data_be_shared=serializer.validated_data.get(
                "can_data_be_shared", False
            ),
        )
        user.set_password(
            serializer.validated_data.get("password")
        )  # Sets the password correctly
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["DELETE"], url_path="delete-account")
    def delete_account(self, request, pk=None):
        """Deletes the user account and all associated data."""
        user = self.get_object()
        user.delete()
        return Response({"status": "Compte supprimé"}, status=status.HTTP_200_OK)
