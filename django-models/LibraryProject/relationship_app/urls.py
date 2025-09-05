from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = "relationship_app"

urlpatterns = [
    path('book_list/', list_books, name='book_list'),
    path('library_details/', LibraryDetailView.as_view(), name='library_details'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
    path("admin_view/", views.admin_view, name="admin_view"),
    path("librarian_view/", views.librarian_view, name="librarian_view"),
    path("member_view/", views.member_view, name="member_view"),
]


