from .models import Book, Author, Librarian, Library

book = Book.objects.get(author = "John")
books = Book.objects.all().get(name="library_name")
library = Library.objects.select_related("librarian").get(name="library_name")