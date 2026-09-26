from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UserRegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user