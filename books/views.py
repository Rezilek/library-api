from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from config.permissions import CanEditAllOrOwner

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [CanEditAllOrOwner]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'authors__first_name', 'authors__last_name', 'genre']
    filterset_fields = ['genre', 'created_by']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_books(self, request):
        """Книги, созданные текущим пользователем"""
        books = Book.objects.filter(created_by=request.user)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
