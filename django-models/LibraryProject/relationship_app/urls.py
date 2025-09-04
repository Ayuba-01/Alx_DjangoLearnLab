from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('book_list/', list_books, name='book_list'),
    path('library_details/', LibraryDetailView.as_view(), name='library_details'),
]