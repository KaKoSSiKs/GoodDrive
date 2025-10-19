# GoodDrive - Облачное хранилище файлов

GoodDrive - это современное веб-приложение для хранения и управления файлами в облаке, построенное на SvelteKit 5 и Django REST Framework.

## 🏗️ Архитектура проекта

```
GoodDrive/
├── frontend/          # SvelteKit 5 + TailwindCSS
├── backend/           # Django + REST Framework
├── nginx/             # Nginx конфигурация
├── docker-compose.yml # Основной Docker Compose
├── docker-compose.dev.yml  # Для разработки
└── docker-compose.prod.yml # Для продакшена
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Node.js 18+ (для локальной разработки фронтенда)
- Python 3.11+ (для локальной разработки бэкенда)
- PostgreSQL (для локальной разработки)

### Запуск в режиме разработки

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd GoodDrive
   ```

2. **Запустите все сервисы через Docker Compose:**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

3. **Или запустите отдельные сервисы:**

   **База данных:**
   ```bash
   docker-compose up db -d
   ```

   **Бэкенд (локально):**
   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

   **Фронтенд (локально):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Запуск в продакшене

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🌐 Доступ к приложению

- **Фронтенд:** http://localhost:3000
- **Бэкенд API:** http://localhost:8000/api
- **Django Admin:** http://localhost:8000/admin
- **Nginx (prod):** http://localhost:80

## 📁 Структура проекта

### Frontend (SvelteKit 5)
- **Технологии:** SvelteKit 5, TailwindCSS, JavaScript
- **Порт:** 3000
- **API URL:** http://localhost:8000/api

### Backend (Django)
- **Технологии:** Django 4.2, Django REST Framework, PostgreSQL
- **Порт:** 8000
- **Приложения:** `files` (управление файлами)

### База данных
- **PostgreSQL 15**
- **Порт:** 5432
- **База:** gooddrive

## 🔧 Конфигурация

### Переменные окружения

**Frontend (.env):**
```
VITE_API_URL=http://localhost:8000/api
```

**Backend (.env):**
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_HOST=localhost
DB_NAME=gooddrive
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🛠️ Команды разработки

### Backend
```bash
# Миграции
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver

# Сбор статических файлов
python manage.py collectstatic
```

### Frontend
```bash
# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшена
npm run build

# Предварительный просмотр сборки
npm run preview
```

## 🐳 Docker команды

```bash
# Сборка всех образов
docker-compose build

# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка всех сервисов
docker-compose down

# Удаление volumes
docker-compose down -v
```

## 📋 API Endpoints

- `GET /api/files/` - Список файлов пользователя
- `POST /api/files/` - Загрузка файла
- `GET /api/files/{id}/` - Получение информации о файле
- `DELETE /api/files/{id}/` - Удаление файла
- `GET /api/files/{id}/download/` - Скачивание файла

## 🔒 Безопасность

- CORS настроен для фронтенда
- Аутентификация через Django REST Framework
- Файлы загружаются в защищенную директорию
- Настройки безопасности для продакшена

## 📝 Лицензия

MIT License

