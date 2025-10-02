from django.urls import path
from .views import (CustomLoginView, CustomLogoutView, registerview, profileview)

app_name = "blog"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", registerview, name="register"),
    path("profile/",  profileview, name="profile")
    
]
