from rest_framework import serializers
from .models import Book, Author, Loan, BookCopy, Member

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'publication_year', 'genre', 'author', 'price', 'edition']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'