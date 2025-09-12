from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("librarian", "Librarian"),
        ("member", "Member"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="member")
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return f"{self.title} — {self.author.name}"
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"), 
            ("can_change_book", "Can change book"), 
            ("can_delete_book", "Can delete book")
        ]
        

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)