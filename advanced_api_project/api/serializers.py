from .models import Book, Author
from rest_framework import serializers
import datetime


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author model"""
    class Meta:
        model = Author
        fields = ["name"]

class BookSerializer(serializers.ModelSerializer):
    """Serializes Book model while nesting AuthorSerializer to display author's name"""
    author = AuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = "__all__"
        
    def validate(self, data):
        if data["publication_year"] > datetime.date.year:
            raise serializers.ValidationError("Publication Year should not be in the future.")
        return data
        