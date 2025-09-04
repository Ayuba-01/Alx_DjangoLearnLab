from .models import Book, Author, Librarian, Library

author = Author.objects.get(name=author_name)
book = Book.objects.filter(name = author)
library = Library.objects.get(name=library_name)
books_qs = library.books.all()
library = Library.objects.select_related("librarian").get(name="library_name")