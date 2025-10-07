# posts/views.py
from rest_framework import viewsets, permissions
from django.db.models import Count
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

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

    # keep author immutable on update 
    def perform_update(self, serializer):
        serializer.save(author=self.get_object().author)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related("author", "post").all()
        post_id = self.request.query_params.get("post")
        return qs.filter(post_id=post_id) if post_id else qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # keep the 'post' immutable on update so users can’t move comments between posts
    def perform_update(self, serializer):
        serializer.save(post=self.get_object().post, author=self.get_object().author)
