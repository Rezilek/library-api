from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book
from authors.models import Author

User = get_user_model()

class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(
            first_name='Лев',
            last_name='Толстой',
            created_by=self.user
        )
    
    def test_create_book(self):
        book = Book.objects.create(
            title='Война и мир',
            isbn='9785699123456',  # Уменьшил длину ISBN
            genre='Роман',
            created_by=self.user
        )
        book.authors.add(self.author)
        
        self.assertEqual(book.title, 'Война и мир')
        self.assertEqual(book.isbn, '9785699123456')
        self.assertEqual(book.created_by, self.user)
        self.assertEqual(book.authors.count(), 1)
    
    def test_book_str(self):
        book = Book.objects.create(
            title='Тестовая книга',
            isbn='1234567890123',
            created_by=self.user
        )
        self.assertEqual(str(book), 'Тестовая книга')


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.author = Author.objects.create(
            first_name='Тест',
            last_name='Автор',
            created_by=self.user
        )
        # Получаем токен для пользователя
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_create_book(self):
        data = {
            'title': 'Новая книга',
            'isbn': '9785123456789',  # 13 символов
            'genre': 'Фантастика',
            'author_ids': [self.author.id]
        }
        response = self.client.post('/api/books/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().created_by, self.user)
    
    def test_list_books(self):
        Book.objects.create(
            title='Книга 1',
            isbn='1111111111111',
            created_by=self.user
        )
        Book.objects.create(
            title='Книга 2',
            isbn='2222222222222',
            created_by=self.other_user
        )
        
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_my_books(self):
        Book.objects.create(
            title='Моя книга',
            isbn='1111111111111',
            created_by=self.user
        )
        Book.objects.create(
            title='Чужая книга',
            isbn='2222222222222',
            created_by=self.other_user
        )
        
        response = self.client.get('/api/books/my_books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Моя книга')
    
    def test_update_own_book(self):
        book = Book.objects.create(
            title='Старое название',
            isbn='3333333333333',
            created_by=self.user
        )
        
        data = {'title': 'Новое название'}
        response = self.client.patch(f'/api/books/{book.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Новое название')
    
    def test_cannot_update_others_book(self):
        book = Book.objects.create(
            title='Чужая книга',
            isbn='4444444444444',
            created_by=self.other_user
        )
        
        data = {'title': 'Попытка изменения'}
        response = self.client.patch(f'/api/books/{book.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Чужая книга')
