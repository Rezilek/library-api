# Library Management API

REST API для управления библиотекой, разработанное на Django Rest Framework.

## 📋 О проекте

API предоставляет возможности для управления книгами, авторами, пользователями и отслеживания выдачи книг.

## 🛠 Технологии

- Python 3.14
- Django 6.0
- Django Rest Framework
- JWT аутентификация
- PostgreSQL
- Docker & Docker Compose
- OpenAPI (Swagger) документация
- Git

## ✨ Функционал

### Управление книгами
- Создание, редактирование, удаление книг
- Получение списка всех книг
- Поиск книг по названию, автору, жанру

### Управление авторами
- CRUD операции для авторов
- Получение списка всех авторов

### Управление пользователями
- Регистрация и авторизация через JWT
- Просмотр информации о пользователях

### Выдача книг
- Запись о выдаче книги пользователю
- Отслеживание статуса возврата
- Автоматическое обновление количества доступных копий

## 🚀 Установка и запуск

### Локальный запуск

1. **Клонировать репозиторий**
   `ash
   git clone <url-репозитория>
   cd library-api-clean
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
Собрать и запустить контейнеры

powershell
docker-compose up --build
Создать суперпользователя (в отдельном терминале)

powershell
docker-compose exec web python manage.py createsuperuser
📚 Документация API
После запуска сервера документация доступна по адресам:

Swagger UI: http://127.0.0.1:8000/api/docs/

OpenAPI schema: http://127.0.0.1:8000/api/schema/

Основные endpoints
Метод	URL	Описание
POST	/api/token/	Получение JWT токена
POST	/api/token/refresh/	Обновление JWT токена
GET/POST	/api/users/	Список/создание пользователей
GET/POST	/api/authors/	Список/создание авторов
GET/POST	/api/books/	Список/создание книг
GET/POST	/api/loans/	Список/создание выдач
POST	/api/loans/{id}/return_book/	Отметка о возврате книги
🔐 Аутентификация
API использует JWT токены. Для доступа к защищенным endpoints необходимо:

Получить токен по адресу /api/token/ (POST) с логином и паролем

Использовать токен в заголовке: Authorization: Bearer <токен>

📊 Структура базы данных
Модели
User - расширенная модель пользователя Django

Author - информация об авторе

Book - информация о книге (связь многие-ко-многим с авторами)

Loan - информация о выдаче книги

🐳 Docker
Проект включает Dockerfile и docker-compose.yml для контейнеризации.

Сборка образа
powershell
docker build -t library-api .
Запуск через Docker Compose
powershell
docker-compose up
👥 Автор
Rezilek

📝 Лицензия
MIT
