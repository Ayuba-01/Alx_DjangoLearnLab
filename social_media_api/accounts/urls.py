from django.urls import path
from .views import ProfileView, RegisterView, FollowUserView, UnfollowUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("follow/<int:user_id>/",   FollowUserView.as_view(),   name="follow"),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow"),  
]
