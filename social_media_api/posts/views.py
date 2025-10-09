from rest_framework import viewsets, permissions, generics, status
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
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


try:
    from notifications.utils import notify
except Exception:
    notify = None 


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects
        .select_related("author")
        .annotate(comment_count=Count("comments"))
        .all()
    )
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.get_object().author)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        POST /api/posts/{pk}/like/
        Idempotent: liking twice keeps one like.
        """
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        # Send a notification to the post author (not for self-like)
        if created and notify and post.author_id != request.user.id:
            notify(recipient=post.author, actor=request.user, verb="liked", target=post)

        return Response(
            {"liked": True, "likes_count": post.likes.count()},
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        POST /api/posts/{pk}/unlike/
        Idempotent: unliking when not liked is a no-op.
        """
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response(
            {"liked": False, "likes_count": post.likes.count()},
            status=status.HTTP_200_OK,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related("author", "post").all()
        post_id = self.request.query_params.get("post")
        return qs.filter(post_id=post_id) if post_id else qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related("author", "post").all()
        post_id = self.request.query_params.get("post")
        return qs.filter(post_id=post_id) if post_id else qs

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)      # capture instance
        post = comment.post
        # Don't notify if the author comments on their own post (optional behavior)
        if post.author_id != self.request.user.id:
            notify(recipient=post.author, actor=self.request.user, verb="commented", target=post)