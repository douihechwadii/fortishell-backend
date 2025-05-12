from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            if User.objects.count() == 0:
                return [AllowAny()]
        return [IsAdminUser()]
    
class AdminExistView(APIView):
    def get(self, request):
        admin_exists = User.objects.filter(is_superuser = True).exists()
        return Response({'admin_exists': admin_exists})
