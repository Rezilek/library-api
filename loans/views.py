from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q
from .models import Loan
from .serializers import LoanSerializer
from config.permissions import CanEditAllOrOwner

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().order_by('-loan_date')
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, CanEditAllOrOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'book__title']
    
    def get_queryset(self):
        """Пользователи видят только свои выдачи, если нет спецправ"""
        user = self.request.user
        if user.has_perm('loans.can_edit_all_loans') or user.is_staff:
            return Loan.objects.all()
        return Loan.objects.filter(Q(user=user) | Q(created_by=user))
    
    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            serializer.save(
                user=self.request.user,
                created_by=self.request.user
            )
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
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Активные выдачи текущего пользователя"""
        loans = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data)
