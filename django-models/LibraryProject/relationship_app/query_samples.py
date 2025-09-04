from .models import Book, Author, Librarian, Library

book = Book.objects.get(author = "John")
books = Library.objects.all(Book)
librarian = Librarian.objects.get(library = "UH")