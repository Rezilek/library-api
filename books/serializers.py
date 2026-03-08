from rest_framework import serializers
from .models import Book
from authors.models import Author

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Author.objects.all(), source='authors'
    )
    
    class Meta:
        model = Book
        fields = '__all__'
