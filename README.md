# Library Management API

REST API для управления библиотекой, разработанное на Django Rest Framework.

## 📋 О проекте

API предоставляет возможности для управления книгами, авторами, пользователями и отслеживания выдачи книг. Реализована JWT аутентификация, система прав доступа и полная документация OpenAPI.

## 🛠 Технологии

- **Python 3.14** - язык программирования
- **Django 6.0** - веб-фреймворк
- **Django Rest Framework** - создание REST API
- **JWT** - аутентификация
- **PostgreSQL** - база данных
- **Docker & Docker Compose** - контейнеризация
- **OpenAPI (Swagger)** - документация
- **django-filter** - фильтрация и поиск
- **Git** - контроль версий

## ✨ Функционал

### Управление книгами
- Создание, редактирование, удаление книг
- Получение списка всех книг
- Поиск книг по названию, автору, жанру
- Просмотр книг, созданных текущим пользователем (/my_books/)

### Управление авторами
- CRUD операции для авторов
- Получение списка всех авторов
- Просмотр авторов, созданных текущим пользователем (/my_authors/)

### Управление пользователями
- Регистрация и авторизация через JWT
- Просмотр информации о пользователях
- Разграничение прав доступа

### Выдача книг
- Запись о выдаче книги пользователю
- Отслеживание статуса возврата
- Автоматическое обновление количества доступных копий
- Просмотр активных выдач (/active/)

## 🔐 Система прав доступа

Реализованы кастомные permissions:

- **IsOwnerOrReadOnly** - чтение для всех, изменение только для владельца
- **CanEditAllOrOwner** - пользователи со спецправами могут редактировать всё
- **IsOwnerOrAdmin** - только владелец или администратор

Администраторы имеют полный доступ ко всем объектам.

## 🗄️ Модели данных

### User (пользователь)
- Расширенная модель Django AbstractUser
- Добавлено поле phone

### Author (автор)
- irst_name, last_name - имя и фамилия
- io - биография
- irth_date - дата рождения
- created_by - ссылка на создателя
- created_at, updated_at - временные метки

### Book (книга)
- 	itle - название
- uthors - связь ManyToMany с авторами
- isbn - уникальный ISBN
- genre - жанр
- 	otal_copies - всего экземпляров
- vailable_copies - доступно сейчас
- created_by - ссылка на создателя
- created_at, updated_at - временные метки

### Loan (выдача)
- user - читатель
- ook - книга
- loan_date - дата выдачи
- due_date - срок возврата
- eturn_date - дата возврата
- status - статус (active/returned/overdue)
- created_by - кто оформил выдачу

## 🚀 Установка и запуск

### Локальный запуск

1. **Клонировать репозиторий**
   `ash
   git clone git@github.com:Rezilek/library-api.git
   cd library-api
Создать и активировать виртуальное окружение

powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
Установить зависимости

powershell
pip install -r requirements.txt
Запустить PostgreSQL в Docker

powershell
docker run --name library-postgres ^
  -e POSTGRES_PASSWORD=postgres ^
  -e POSTGRES_DB=library ^
  -p 5436:5432 ^
  -d postgres:15
Применить миграции

powershell
python manage.py migrate
Создать суперпользователя

powershell
python manage.py createsuperuser
Запустить сервер

powershell
python manage.py runserver
Запуск через Docker Compose
powershell
docker-compose up --build
В отдельном терминале создать суперпользователя:

powershell
docker-compose exec web python manage.py createsuperuser
📚 Документация API
После запуска сервера документация доступна по адресам:

Swagger UI: http://127.0.0.1:8000/api/docs/

OpenAPI schema: http://127.0.0.1:8000/api/schema/

#####Основные endpoints
####Аутентификация
Метод	URL	Описание
POST	/api/token/	Получение JWT токена
POST	/api/token/refresh/	Обновление JWT токена
######Пользователи
Метод	URL	Описание
POST	/api/users/	Регистрация (доступно без токена)
GET	/api/users/	Список пользователей
GET	/api/users/{id}/	Детали пользователя
######Авторы
Метод	URL	Описание
GET	/api/authors/	Список авторов
POST	/api/authors/	Создание автора
GET	/api/authors/my_authors/	Мои авторы
GET	/api/authors/{id}/	Детали автора
PUT/PATCH	/api/authors/{id}/	Обновление автора
DELETE	/api/authors/{id}/	Удаление автора
######Книги
Метод	URL	Описание
GET	/api/books/	Список книг (с поиском)
POST	/api/books/	Создание книги
GET	/api/books/my_books/	Мои книги
GET	/api/books/{id}/	Детали книги
PUT/PATCH	/api/books/{id}/	Обновление книги
DELETE	/api/books/{id}/	Удаление книги
######Выдачи
Метод	URL	Описание
GET	/api/loans/	Список выдач
POST	/api/loans/	Создание выдачи
GET	/api/loans/active/	Активные выдачи
POST	/api/loans/{id}/return_book/	Возврат книги
🔍 Поиск и фильтрация
######Поиск книг
text
GET /api/books/?search=война
Поиск по: названию, имени автора, фамилии автора, жанру

######Фильтрация по жанру
text
GET /api/books/?genre=Роман
Фильтрация по создателю
text
GET /api/books/?created_by=1
🧪 Тестирование
Проект покрыт тестами (13 тестов):

powershell
# Запустить все тесты
python manage.py test

# Запустить тесты конкретного приложения
python manage.py test books
python manage.py test users
Что тестируется:
✅ Создание моделей

✅ Права доступа

✅ API endpoints

✅ Аутентификация

✅ Валидация данных

🐳 Docker
Dockerfile
dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
Docker Compose
yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: library
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5436:5432"
  
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DB_NAME: library
      DB_USER: postgres
      DB_PASSWORD: postgres
      DB_HOST: db
      DB_PORT: 5432
📊 Примеры запросов
Получение токена
bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
Создание книги (с токеном)
bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Война и мир",
    "isbn": "9785699123456",
    "genre": "Роман",
    "author_ids": [1]
  }'
Поиск книг
bash
curl -X GET "http://localhost:8000/api/books/?search=война" \
  -H "Authorization: Bearer <your_token>"
Мои книги
bash
curl -X GET http://localhost:8000/api/books/my_books/ \
  -H "Authorization: Bearer <your_token>"
Создание выдачи
bash
curl -X POST http://localhost:8000/api/loans/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "due_date": "2026-04-10"
  }'
Возврат книги
bash
curl -X POST http://localhost:8000/api/loans/1/return_book/ \
  -H "Authorization: Bearer <your_token>"
👥 Автор
Rezilek

GitHub: @Rezilek

Проект: library-api

📝 Лицензия
MIT License - свободное использование, модификация и распространение.

Проект выполнен в рамках дипломной работы.
