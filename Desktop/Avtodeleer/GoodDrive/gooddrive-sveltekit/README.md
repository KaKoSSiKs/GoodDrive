# GoodDrive - SvelteKit 5 + Prisma + MySQL

Монолитное full-stack приложение для интернет-магазина автозапчастей.

## 🚀 Технологии

- **Frontend/Backend**: SvelteKit 5
- **Database**: MySQL
- **ORM**: Prisma
- **Auth**: JWT (jsonwebtoken)
- **UI**: Tailwind CSS + Lucide Icons
- **Runtime**: Node.js 20+

## 📦 Установка

### 1. Установка зависимостей

```bash
npm install
```

### 2. Настройка окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите параметры MySQL:

```env
DATABASE_URL="mysql://user:password@localhost:3306/gooddrive"
JWT_SECRET="your-secret-key"
```

### 3. Инициализация базы данных

```bash
# Применить миграции Prisma
npx prisma migrate dev --name init

# Сгенерировать Prisma Client
npx prisma generate
```

## 🔄 Миграция данных из PostgreSQL

Если у вас есть данные в PostgreSQL (Django), выполните миграцию:

### Шаг 1: Экспорт данных из PostgreSQL

Перейдите в директорию Django backend и выполните:

```bash
cd ../backend
python ../gooddrive-sveltekit/scripts/export-from-postgres.py
```

Это создаст файл `scripts/exported-data.json` с данными.

### Шаг 2: Импорт в MySQL

```bash
node scripts/migrate-data.js
```

## 🏃 Запуск

### Development

```bash
npm run dev
```

Приложение будет доступно на `http://localhost:3000`

### Production Build

```bash
npm run build
npm run preview
```

## 📋 Структура проекта

```
gooddrive-sveltekit/
├── prisma/
│   └── schema.prisma          # Схема БД
├── src/
│   ├── lib/
│   │   ├── server/
│   │   │   ├── auth.ts        # Аутентификация
│   │   │   └── db.ts          # Prisma client
│   │   └── types.ts           # TypeScript типы
│   ├── routes/
│   │   ├── api/               # API endpoints
│   │   │   ├── auth/
│   │   │   ├── brands/
│   │   │   ├── parts/
│   │   │   ├── orders/
│   │   │   └── ...
│   │   ├── catalog/           # Страница каталога
│   │   ├── cart/              # Корзина
│   │   ├── admin/             # Админ панель
│   │   └── +layout.svelte     # Главный layout
│   ├── app.css                # Стили
│   └── hooks.server.ts        # Server hooks (auth)
├── scripts/
│   ├── export-from-postgres.py
│   └── migrate-data.js
└── package.json
```

## 🔑 API Endpoints

### Аутентификация
- `POST /api/auth/login` - Вход
- `POST /api/auth/logout` - Выход
- `GET /api/auth/verify` - Проверка токена

### Каталог
- `GET /api/brands` - Список брендов
- `GET /api/warehouses` - Список складов
- `GET /api/parts` - Список запчастей (с фильтрами)
- `GET /api/parts/[id]` - Информация о запчасти

### Заказы
- `GET /api/orders` - Список заказов (admin)
- `POST /api/orders` - Создать заказ
- `GET /api/orders/[id]` - Информация о заказе

## 🔒 Аутентификация

Используется JWT токен, хранящийся в httpOnly cookie.

### Создание первого администратора

```bash
npx prisma studio
```

Откройте таблицу `users` и создайте пользователя вручную (пароль нужно захешировать bcrypt).

Или используйте seed скрипт (создайте `prisma/seed.js`).

## 🚀 Деплой

### Vercel + PlanetScale

1. Подключите MySQL на PlanetScale
2. Добавьте `DATABASE_URL` в Vercel Environment Variables
3. Deploy!

### VPS (Ubuntu/Debian)

```bash
# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install MySQL
sudo apt-get install mysql-server

# Clone and setup
git clone <repo>
cd gooddrive-sveltekit
npm install
npx prisma migrate deploy
npm run build

# Run with PM2
npm install -g pm2
pm2 start build/index.js --name gooddrive
```

## 📝 Полезные команды

```bash
# Prisma
npx prisma studio          # GUI для БД
npx prisma migrate dev     # Создать миграцию
npx prisma generate        # Обновить Prisma Client

# Development
npm run dev                # Dev server
npm run build              # Production build
npm run preview            # Preview production

# Database
npm run db:seed            # Заполнить тестовыми данными
```

## 🛠️ Разработка

### Добавление новой модели

1. Обновите `prisma/schema.prisma`
2. Создайте миграцию: `npx prisma migrate dev --name add_model`
3. Создайте API endpoint в `src/routes/api/`
4. Создайте frontend страницу

### Изменение схемы БД

```bash
npx prisma migrate dev --name change_description
```

## 📄 Лицензия

Частный проект.

