from django.urls import path
from .views import (CustomLoginView, CustomLogoutView, registerview, profileview, PostListView, 
                    PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,CommentCreateView, CommentUpdateView, CommentDeleteView,)

app_name = "blog"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", registerview, name="register"),
    path("profile/",  profileview, name="profile"),
    
    path("posts/",                    PostListView.as_view(),   name="post-list"),
    path("post/new/",                PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/",           PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/",      PostUpdateView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/",    PostDeleteView.as_view(), name="post-delete"),
    
    path("post/<int:pk>/comments/new/",   CommentCreateView.as_view(),  name="comment-create"),
    path("comment/<int:pk>/update/",             CommentUpdateView.as_view(),  name="comment-edit"),
    path("comment/<int:pk>/delete/",           CommentDeleteView.as_view(),  name="comment-delete"),
    
]
