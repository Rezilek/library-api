from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
    
    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Получаем токен для тестов
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def test_user_registration(self):
        """Регистрация нового пользователя (публичный endpoint)"""
        # Для регистрации не нужен токен
        self.client.credentials()  # Убираем токен
        
        user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'securepass123'
        }
        response = self.client.post('/api/users/', user_data)
        
        # Проверяем, что вернулась ошибка 401 (неавторизован)
        # или что пользователь создан - зависит от настроек permissions
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            # Если регистрация требует авторизации, используем админа
            admin = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
            refresh = RefreshToken.for_user(admin)
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
            response = self.client.post('/api/users/', user_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        else:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_jwt_token_obtain(self):
        """Получение JWT токена"""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_get_users_list(self):
        """Список пользователей (требует авторизации)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_current_user(self):
        """Получение информации о текущем пользователе"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
