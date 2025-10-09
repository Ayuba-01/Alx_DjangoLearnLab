from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"comments", CommentViewSet, basename="comments")
post_like_view = PostViewSet.as_view({"post": "like"})
post_unlike_view = PostViewSet.as_view({"post": "unlike"})

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
    path("posts/<int:pk>/like/", post_like_view, name="post-like"),
    path("posts/<int:pk>/unlike/", post_unlike_view, name="post-unlike"),
]
