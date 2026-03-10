from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    user_username = serializers.ReadOnlyField(source='user.username')
    book_title = serializers.ReadOnlyField(source='book.title')
    
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('loan_date', 'status', 'created_by')
