from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Gets the serializer
        serializer.is_valid(raise_exception=True)  # Checks if the data is valid

        age = serializer.validated_data.get('age')
        if age is not None and int(age) < 15:
            return Response({'error': 'Un utilisateur de moins de 15 ans ne peut pas s\'inscrire.'}, status=400)
        user = User(username=serializer.validated_data.get('username'), email=serializer.validated_data.get('email'), age=age)
        user.set_password(serializer.validated_data.get('password'))  # Sets the password correctly
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['DELETE'], url_path='delete-account')
    def delete_account(self, request, pk=None):
        user = self.get_object()
        user.delete()  # Supprime l'utilisateur et toutes ses données associées
        return Response({'status': 'Compte supprimé'}, status=status.HTTP_200_OK)