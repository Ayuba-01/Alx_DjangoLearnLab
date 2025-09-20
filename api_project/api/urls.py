from django.urls import path, include
from .views import BookList, BookViewSet, RegisterView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r"books_all", BookViewSet, basename="book_all")

urlpatterns = [
    path("", include(router.urls)),
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
    path("auth/token/", obtain_auth_token, name="obtain_auth_token"),
    path("auth/register/", RegisterView.as_view(), name="register"),
]