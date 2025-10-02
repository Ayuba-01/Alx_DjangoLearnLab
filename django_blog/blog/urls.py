from django.urls import path
from .views import (CustomLoginView, CustomLogoutView, registerview, profileview, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView)

app_name = "blog"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", registerview, name="register"),
    path("profile/",  profileview, name="profile"),
    
    path("posts/",                    PostListView.as_view(),   name="post-list"),
    path("posts/new/",                PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/",           PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/",      PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/",    PostDeleteView.as_view(), name="post-delete"),
    
]
