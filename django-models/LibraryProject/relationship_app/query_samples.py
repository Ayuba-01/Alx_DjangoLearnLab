from .models import Book, Author, Librarian, Library

book = Book.objects.get(author = "John")
books = Library.objects.get(name="library_name"), 
librarian = Librarian.objects.get(library = "UH")