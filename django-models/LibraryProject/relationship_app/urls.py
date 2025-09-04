from django.urls import path
from .views import book_list, LibraryDetails

urlpatterns = [
    path('book_list/', book_list, name='book_list'),
    path('library_details/', LibraryDetails.as_view(), name='library_details'),
]