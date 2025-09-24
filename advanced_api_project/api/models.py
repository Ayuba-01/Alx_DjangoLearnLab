from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        pass

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=250)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    class Meta:
        pass

    def __str__(self):
        return self.name
