from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
