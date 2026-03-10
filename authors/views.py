from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer
from config.permissions import CanEditAllOrOwner

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('-created_at')
    serializer_class = AuthorSerializer
    permission_classes = [CanEditAllOrOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_authors(self, request):
        """Авторы, созданные текущим пользователем"""
        authors = Author.objects.filter(created_by=request.user)
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)
