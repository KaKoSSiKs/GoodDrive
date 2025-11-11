# 🎯 Что можно делать в приложении

## 📱 Для пользователей

### 1. Просмотр каталога
Откройте: **http://localhost:3000/catalog**

- Просмотр всех 100 товаров
- Поиск по названию, артикулу
- Фильтрация (в разработке)

### 2. Просмотр товара
Кликните на любой товар в каталоге

- Детальная информация
- Изображение
- Цена и наличие
- Кнопка "В корзину"

### 3. Корзина
Откройте: **http://localhost:3000/cart**

- Управление количеством
- Расчёт суммы
- Переход к оформлению

### 4. Оформление заказа
Откройте: **http://localhost:3000/checkout**

- Заполнение данных клиента
- Адрес доставки
- Создание заказа

---

## 👨‍💼 Для администраторов

### 1. Вход в админку
Откройте: **http://localhost:3000/admin**

**Credentials:**
- Email: `admin@gooddrive.com`
- Password: `admin123`

### 2. Управление данными через Prisma Studio

```bash
cd gooddrive-sveltekit
npx prisma studio
```

Откроется GUI на http://localhost:5555

**Что можно делать:**
- Просматривать все таблицы
- Редактировать записи
- Добавлять новые товары
- Удалять записи
- Экспортировать данные

---

## 🔍 Тестирование API

### Через curl (PowerShell)

**Получить все бренды:**
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/brands" -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | Format-List
```

**Получить товары:**
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/parts?page=1&page_size=5" -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

**Поиск товара:**
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/parts?search=фильтр" -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

**Войти как админ:**
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/auth/login" -Method POST -ContentType "application/json" -Body '{"email":"admin@gooddrive.com","password":"admin123"}' -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

---

## 🛠️ Управление проектом

### Остановить сервер
В терминале где запущен `npm run dev`:
```
Ctrl+C
```

### Перезапустить
```bash
cd D:\study\GoodDrive\gooddrive-sveltekit
npm run dev
```

### Остановить MySQL
```bash
docker stop gooddrive-mysql
```

### Запустить MySQL
```bash
docker start gooddrive-mysql
```

### Просмотр логов MySQL
```bash
docker logs gooddrive-mysql
```

---

## 📦 Добавление данных

### Импортировать больше товаров из CSV

Откройте `scripts/import-from-csv.js` и измените лимит:

```javascript
const limit = 500; // Вместо 100
```

Затем:
```bash
node scripts/import-from-csv.js
```

### Добавить товар вручную

```bash
npx prisma studio
```

1. Откройте таблицу `catalog_parts`
2. Нажмите "Add record"
3. Заполните поля
4. Save

---

## 🧪 Тестирование функций

### Создание заказа через API

```powershell
$order = @{
    customerName = "Иван Иванов"
    customerPhone = "+79991234567"
    customerEmail = "test@example.com"
    deliveryAddress = "ул. Тестовая, д. 1"
    deliveryCity = "Москва"
    notes = "Тестовый заказ"
    items = @(
        @{
            partId = 1
            title = "Тестовый товар"
            price = 1000
            quantity = 2
        }
    )
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:3000/api/orders" -Method POST -ContentType "application/json" -Body $order -UseBasicParsing
```

---

## 📊 Просмотр данных в MySQL

```bash
# Войти в MySQL контейнер
docker exec -it gooddrive-mysql mysql -u root -p
# Password: password
```

```sql
USE gooddrive_new;

-- Посмотреть товары
SELECT id, title, price_opt FROM catalog_parts LIMIT 10;

-- Посмотреть бренды
SELECT * FROM catalog_brands;

-- Посмотреть заказы
SELECT * FROM orders;
```

---

## 🎨 Кастомизация

### Изменить цвета темы

Откройте `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#your-color',
        600: '#your-darker-color',
        // ...
      }
    }
  }
}
```

### Изменить порт

Откройте `vite.config.ts`:

```typescript
server: {
  port: 3001, // Ваш порт
  host: true
}
```

---

## ⚡ Горячие клавиши в разработке

- `Ctrl+C` - Остановить dev сервер
- `Ctrl+Shift+R` - Перезагрузить страницу без кэша
- `F12` - DevTools
- `Ctrl+K` - Поиск в Prisma Studio

---

## 📈 Следующие шаги

1. ✅ Проект запущен и работает
2. 📝 Ознакомьтесь с кодом в `src/routes/`
3. 🎨 Настройте дизайн под себя
4. 🔧 Добавьте нужные функции
5. 🚀 Подготовьте к деплою

---

**Проект полностью готов к работе!** 🎉

