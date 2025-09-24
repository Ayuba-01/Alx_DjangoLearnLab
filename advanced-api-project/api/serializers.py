from datetime import date
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Serializes Book model while nesting AuthorSerializer to display author's name"""
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author model"""
    # Use related_name='books' on the FK; otherwise use 'book_set'
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
