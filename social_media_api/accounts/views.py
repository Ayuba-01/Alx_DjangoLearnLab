from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import action


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)
    