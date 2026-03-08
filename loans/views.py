from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Loan
from .serializers import LoanSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError('Нет доступных копий')
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.status == 'active':
            loan.status = 'returned'
            loan.return_date = timezone.now()
            loan.save()
            book = loan.book
            book.available_copies += 1
            book.save()
            return Response({'status': 'book returned'})
        return Response({'error': 'book already returned'}, status=400)
