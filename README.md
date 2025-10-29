# GoodDrive - Интернет-магазин автозапчастей

GoodDrive - это современный интернет-магазин автозапчастей с каталогом, корзиной, системой заказов и SEO-оптимизацией, построенный на SvelteKit 5 и Django REST Framework.

## 🏗️ Архитектура проекта

```
GoodDrive/
├── frontend/          # SvelteKit 5 + TailwindCSS
├── backend/           # Django + REST Framework
├── nginx/             # Nginx конфигурация
├── documentation/     # Техническая документация
├── docker-compose.yml # Основной Docker Compose
├── docker-compose.dev.yml  # Для разработки
└── docker-compose.prod.yml # Для продакшена
```

## ✨ Основные функции

### 🛒 Интернет-магазин
- **Каталог автозапчастей** с фильтрацией по брендам, ценам, наличию
- **Поиск** по названию, номеру детали, производителю
- **Корзина покупок** с сохранением в localStorage
- **Система заказов** с отслеживанием статусов
- **Управление складскими остатками**

### 🎨 Пользовательский интерфейс
- **Адаптивный дизайн** для всех устройств
- **SvelteKit 5** с современными рунами
- **TailwindCSS** для стилизации
- **Компонентная архитектура**

### 🔧 Технические возможности
- **REST API** на Django REST Framework
- **SEO-оптимизация** с мета-тегами и JSON-LD
- **Пагинация** и фильтрация данных
- **Docker** для контейнеризации
- **PostgreSQL** для хранения данных

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

### Основные команды

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

### Перезапуск после внесения изменений

После изменения кода необходимо перезапустить соответствующие контейнеры:

**Перезапуск всех контейнеров:**
```bash
docker-compose -f docker-compose.dev.yml restart
```

**Пересборка и перезапуск всех контейнеров (после изменений в Dockerfile):**
```bash
docker-compose -f docker-compose.dev.yml up --build -d
```

**Перезапуск конкретного сервиса:**
```bash
# Только фронтенд
docker-compose -f docker-compose.dev.yml restart frontend

# Только бэкенд
docker-compose -f docker-compose.dev.yml restart backend

# Только база данных
docker-compose -f docker-compose.dev.yml restart db
```

**Полная пересборка конкретного сервиса (с удалением старого образа):**
```bash
# Удалить старый контейнер и образ фронтенда
docker-compose -f docker-compose.dev.yml rm -f frontend
docker rmi gooddrive-frontend

# Пересобрать и запустить
docker-compose -f docker-compose.dev.yml up --build -d frontend
```

**Просмотр логов конкретного сервиса:**
```bash
# Логи фронтенда
docker-compose -f docker-compose.dev.yml logs -f frontend

# Логи бэкенда
docker-compose -f docker-compose.dev.yml logs -f backend
```

**После изменений в Python/Django коде:**
```bash
# Перезапуск бэкенда
docker-compose -f docker-compose.dev.yml restart backend

# Или если нужны миграции
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
```

**После изменений в JavaScript/Svelte коде:**
```bash
# Перезапуск фронтенда
docker-compose -f docker-compose.dev.yml restart frontend

# Или полная пересборка (если изменился package.json)
docker-compose -f docker-compose.dev.yml up --build -d frontend
```

**Очистка и полный перезапуск (если что-то работает неправильно):**
```bash
# Остановить и удалить все контейнеры
docker-compose -f docker-compose.dev.yml down

# Удалить неиспользуемые образы
docker system prune -a

# Полная пересборка с нуля
docker-compose -f docker-compose.dev.yml up --build
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


