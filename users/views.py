from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        age = request.data.get('age')
        if age is not None and int(age) < 15:
            return Response({'error': 'Un utilisateur de moins de 15 ans ne peut pas s\'inscrire.'}, status=400)
        return super().create(request, *args, **kwargs)
