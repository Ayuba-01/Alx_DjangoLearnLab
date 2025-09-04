from .models import Book, Author, Librarian, Library

author = Author.objects.get(name=author_name)
book = Book.objects.filter(author=author)
library = Library.objects.get(name=library_name)
books_qs = library.books.all()
librarian = Librarian.objects.get(library="library_name")