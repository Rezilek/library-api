from users.models import User
from django.contrib.auth.hashers import make_password

# Проверяем, есть ли уже admin
if User.objects.filter(username='admin').exists():
    print('Пользователь admin уже существует')
else:
    # Создаем нового пользователя
    user = User(
        username='admin',
        email='admin@example.com',
        is_staff=True,
        is_superuser=True,
        password=make_password('admin123')
    )
    user.save()
    print('Суперпользователь admin успешно создан!')

# Показываем всех пользователей
print(f'Всего пользователей: {User.objects.count()}')
for u in User.objects.all():
    print(f' - {u.username} (superuser: {u.is_superuser})')
