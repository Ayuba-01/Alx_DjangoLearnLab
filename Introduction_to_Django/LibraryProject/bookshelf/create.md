In [1]: new_book = Book.objects.create(title = "1984", author = "George Orwell", publication_year = "1949")

In [2]: new_book.save()