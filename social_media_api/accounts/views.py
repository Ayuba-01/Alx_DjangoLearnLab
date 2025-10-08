from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework import generics, permissions, viewsets, mixins, status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        target = get_object_or_404(self.get_queryset(), pk=user_id)
        # current user follows target (reverse accessor from your M2M)
        request.user.following.add(target)
        return Response({
            "following": True,
            "following_count": request.user.following.count(),
            "target_followers_count": target.followers.count(),
        }, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        target = get_object_or_404(self.get_queryset(), pk=user_id)
        request.user.following.remove(target)
        return Response({
            "following": False,
            "following_count": request.user.following.count(),
            "target_followers_count": target.followers.count(),
        }, status=status.HTTP_200_OK)
