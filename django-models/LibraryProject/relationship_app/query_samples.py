from .models import Book, Author, Librarian, Library

book = Book.objects.get(author = "John")
library = Library.objects.get(name="library_name")
books_qs = library.books.all()
library = Library.objects.select_related("librarian").get(name="library_name")