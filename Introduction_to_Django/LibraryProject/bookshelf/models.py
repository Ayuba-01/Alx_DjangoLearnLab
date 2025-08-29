from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    
    @classmethod
    def create(cls, title, author, publication_year):
        book = cls(title=title, author=author, publication_year=publication_year)
        return book
    
    
