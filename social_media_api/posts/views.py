# posts/views.py
from rest_framework import viewsets, permissions, generics
from django.db.models import Count
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.all()
    )
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # keep author immutable on update 
    def perform_update(self, serializer):
        serializer.save(author=self.get_object().author)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.all()
        post_id = self.request.query_params.get("post")
        return qs.filter(post_id=post_id) if post_id else qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # keep the 'post' immutable on update so users can’t move comments between posts
    def perform_update(self, serializer):
        serializer.save(post=self.get_object().post, author=self.get_object().author)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return (
            Post.objects.filter(author__in=following_users).order_by("-created_at")
            .select_related("author")
        )