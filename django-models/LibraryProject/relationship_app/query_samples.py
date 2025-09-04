from .models import Book, Author, Librarian, Library

author = Author.objects.filter(author__name=author_name)
book = Book.objects.get(name = author_name)
library = Library.objects.get(name=library_name)
books_qs = library.books.all()
library = Library.objects.select_related("librarian").get(name="library_name")