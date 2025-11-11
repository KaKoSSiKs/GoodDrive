# 🚀 Быстрый старт GoodDrive SvelteKit

## За 5 минут до запуска!

### ✅ Шаг 1: Установка (1 мин)

```bash
cd gooddrive-sveltekit
npm install
```

### ✅ Шаг 2: Настройка БД (2 мин)

**Вариант A: Использовать существующие данные Django**

```bash
# 1. Экспорт из PostgreSQL
cd ../backend
python ../gooddrive-sveltekit/scripts/export-from-postgres.py

# 2. Настройка MySQL
# Создайте БД в MySQL
mysql -u root -p
```

```sql
CREATE DATABASE gooddrive CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

```bash
# 3. Настройте .env
cd ../gooddrive-sveltekit
cp .env.example .env
nano .env  # Измените DATABASE_URL
```

```env
DATABASE_URL="mysql://root:password@localhost:3306/gooddrive"
JWT_SECRET="your-super-secret-key-min-32-chars-long"
```

```bash
# 4. Применить миграции
npx prisma migrate dev --name init

# 5. Импортировать данные
node scripts/migrate-data.js
```

**Вариант B: Начать с чистой БД**

```bash
# 1. Создать .env
cp .env.example .env
nano .env

# 2. Применить миграции
npx prisma migrate dev --name init

# 3. Заполнить начальными данными
npm run db:seed
```

### ✅ Шаг 3: Запуск (30 сек)

```bash
npm run dev
```

Готово! Откройте http://localhost:3000

**Credentials:**
- Email: `admin@gooddrive.com`
- Password: `admin123`

---

## 📊 Проверка работы

### Проверка данных в БД

```bash
# Открыть Prisma Studio
npx prisma studio
```

Откроется GUI на http://localhost:5555

### Проверка API

**Brands:**
```bash
curl http://localhost:3000/api/brands | jq
```

**Parts (каталог):**
```bash
curl "http://localhost:3000/api/parts?page=1&page_size=10" | jq
```

**Конкретная запчасть:**
```bash
curl http://localhost:3000/api/parts/2 | jq
```

### Проверка авторизации

```bash
# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gooddrive.com","password":"admin123"}' | jq

# Verify (используйте токен из ответа выше)
curl http://localhost:3000/api/auth/verify \
  -H "Cookie: auth_token=YOUR_TOKEN_HERE" | jq
```

---

## 🎯 Основные маршруты

| URL | Описание |
|-----|----------|
| `/` | Главная страница |
| `/catalog` | Каталог автозапчастей |
| `/product/[id]` | Страница товара |
| `/cart` | Корзина |
| `/checkout` | Оформление заказа |
| `/admin` | Админ панель |

---

## 🔧 Полезные команды

```bash
# Development
npm run dev              # Запуск dev сервера
npm run build            # Production build
npm run preview          # Предпросмотр production

# Prisma
npx prisma studio        # GUI для БД
npx prisma migrate dev   # Создать миграцию
npx prisma generate      # Обновить Prisma Client
npx prisma migrate reset # Сбросить БД (осторожно!)

# Database
npm run db:seed          # Заполнить начальными данными
node scripts/migrate-data.js  # Импорт из PostgreSQL
```

---

## 🐛 Решение проблем

### Ошибка подключения к MySQL

```bash
# Проверить, запущен ли MySQL
sudo systemctl status mysql

# Запустить MySQL
sudo systemctl start mysql
```

### Prisma не генерирует Client

```bash
rm -rf node_modules
npm install
npx prisma generate
```

### "MODULE_NOT_FOUND" ошибки

```bash
npm install
```

### Порт 3000 занят

Измените в `vite.config.ts`:

```ts
server: {
  port: 3001,  // Другой порт
  host: true
}
```

---

## 📈 Следующие шаги

1. **Кастомизация**: Измените цвета в `tailwind.config.js`
2. **Добавление функций**: Создайте новые API routes
3. **Деплой**: Следуйте `MIGRATION_GUIDE.md` → раздел "Деплой"

---

## 📞 Поддержка

- **Документация**: `README.md` и `MIGRATION_GUIDE.md`
- **Prisma Docs**: https://www.prisma.io/docs
- **SvelteKit Docs**: https://kit.svelte.dev/docs

---

## ✅ Чек-лист

- [ ] npm install выполнен
- [ ] MySQL установлен и запущен
- [ ] .env создан и настроен
- [ ] Prisma миграции применены
- [ ] Данные импортированы (или seed выполнен)
- [ ] npm run dev запускается без ошибок
- [ ] http://localhost:3000 открывается
- [ ] API возвращает данные
- [ ] Можно залогиниться как admin

**Всё работает? Поздравляем! 🎉**

