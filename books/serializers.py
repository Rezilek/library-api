from rest_framework import serializers
from .models import Book
from authors.models import Author
from authors.serializers import AuthorSerializer

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Author.objects.all(), source='authors'
    )
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
