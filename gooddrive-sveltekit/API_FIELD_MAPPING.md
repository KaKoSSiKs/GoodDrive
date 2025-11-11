# 📊 API FIELD MAPPING - snake_case vs camelCase

**Дата:** 11 ноября 2025  
**Статус:** 🟢 Все поля совместимы  

---

## 🎯 СТРАТЕГИЯ ИМЕНОВАНИЯ

### Принятая стратегия:
- **Backend Prisma модели:** camelCase (TypeScript стандарт)
- **API Response:** Смешанный подход для совместимости
  - Некоторые endpoints возвращают camelCase (новые)
  - Некоторые возвращают snake_case (совместимость)
  - Некоторые возвращают оба формата

---

## 📋 ТАБЛИЦА МАППИНГА

### Orders (заказы)

| Frontend использует | API возвращает | Prisma модель |
|-------------------|----------------|---------------|
| `orderNumber` | `orderNumber` | `orderNumber` |
| `customerName` | `customerName` | `customerName` |
| `customerPhone` | `customerPhone` | `customerPhone` |
| `customerEmail` | `customerEmail` | `customerEmail` |
| `deliveryAddress` | `deliveryAddress` | `deliveryAddress` |
| `deliveryCity` | `deliveryCity` | `deliveryCity` |
| `deliveryPostalCode` | `deliveryPostalCode` | `deliveryPostalCode` |
| `totalAmount` | `totalAmount` | `totalAmount` |
| `itemsCount` | `itemsCount` | computed |
| `createdAt` | `createdAt` | `createdAt` |
| `updatedAt` | `updatedAt` | `updatedAt` |

**Endpoints:**
- `GET /api/orders` → camelCase
- `GET /api/orders/[id]` → camelCase

---

### Parts (товары)

| Frontend использует | API возвращает | Prisma модель |
|-------------------|----------------|---------------|
| `id` | `id` | `id` |
| `title` | `title` | `title` |
| `original_number` | `original_number` | `originalNumber` |
| `manufacturer_number` | `manufacturer_number` | `manufacturerNumber` |
| `brand_name` | `brand_name` | `brand.name` (computed) |
| `warehouse_name` | `warehouse_name` | `warehouse.name` (computed) |
| `brand` | `brand` | `brand` (relation) |
| `warehouse` | `warehouse` | `warehouse` (relation) |
| `price_opt` | `price_opt` (string) | `priceOpt` (Decimal) |
| `cost_price` | `cost_price` (string) | `costPrice` (Decimal) |
| `available` | `available` | `available` |
| `stock` | `stock` | `stock` |
| `reserve` | `reserve` | `reserve` |
| `images` | `images` | `images` (relation) |
| `created_at` | `created_at` | `createdAt` |
| `updated_at` | `updated_at` | `updatedAt` |

**Images вложенность:**
- `images[0].image_url` → `images[0].imageUrl` (в Prisma)
- `images[0].alt_text` → `images[0].altText` (в Prisma)

**Endpoints:**
- `GET /api/parts` → snake_case (для совместимости)
- `GET /api/parts/[id]` → snake_case (для совместимости)

---

### Customers (клиенты)

| Frontend использует | API возвращает | Prisma модель |
|-------------------|----------------|---------------|
| `id` | `id`, `id` | `id` |
| `name` | `name`, `name` | `name` |
| `phone` | `phone`, `phone` | `phone` |
| `email` | `email`, `email` | `email` |
| `city` | `city`, `city` | `city` |
| `address` | `address`, `address` | `address` |
| `category` | `category`, `category` | `category` |
| `total_orders` | `totalOrders`, `total_orders` | `totalOrders` |
| `total_spent` | `totalSpent`, `total_spent` | `totalSpent` |
| `average_order` | `averageOrder`, `average_order` | `averageOrder` |
| `last_order_date` | `lastOrderDate`, `last_order_date` | `lastOrderDate` |
| `created_at` | `createdAt`, `created_at` | `createdAt` |

**Endpoints:**
- `GET /api/crm/customers` → **оба формата** (максимальная совместимость)

---

### Finance Summary (финансы)

| Frontend использует | API возвращает | Источник данных |
|-------------------|----------------|----------------|
| `revenue` | `revenue` | Сумма завершенных заказов |
| `expenses` | `expenses` | Сумма расходов |
| `profit` | `profit` | revenue - expenses |
| `gross_profit` | `gross_profit` | revenue - cost_of_goods |
| `net_profit` | `net_profit` | gross_profit - operating_expenses |
| `cost_of_goods` | `cost_of_goods` | revenue × 0.6 (расчетное) |
| `operating_expenses` | `operating_expenses` | Сумма расходов |
| `margin_percent` | `margin_percent` | (gross_profit / revenue) × 100 |
| `orders_count` | `orders_count` | Количество завершенных заказов |
| `average_order` | `average_order` | revenue / orders_count |

**Endpoints:**
- `GET /api/finance/summary` → snake_case

---

### Analytics (аналитика)

| Frontend использует | API возвращает | Источник |
|-------------------|----------------|----------|
| `total` | `total` | Все заказы |
| `new` | `new` | Заказы со статусом "new" |
| `processing` | `processing` | Заказы со статусом "processing" |
| `completed` | `completed` | Заказы со статусом "completed" |
| `canceled` | `canceled` | Заказы со статусом "canceled" |
| `lastWeek` | `lastWeek` | Заказы за последние 7 дней |
| `ordersByDay` | `ordersByDay` | Группировка по датам |
| `averageOrder` | `averageOrder` | Средний чек |
| `totalRevenue` | `totalRevenue` | Общая выручка |

**Endpoints:**
- `GET /api/analytics/orders` → camelCase

---

## 🔧 РЕКОМЕНДАЦИИ ПО ИСПОЛЬЗОВАНИЮ

### Для новых компонентов:
Используйте **camelCase** (JavaScript стандарт):
```javascript
order.orderNumber
order.customerName
order.totalAmount
```

### Для старых компонентов (из Django):
Используйте **snake_case** (если API поддерживает):
```javascript
part.original_number
part.brand_name
part.price_opt
```

### Для максимальной совместимости:
Используйте проверки на оба формата:
```javascript
order.orderNumber || order.order_number
customer.totalOrders || customer.total_orders
```

---

## ✅ ТЕКУЩИЙ СТАТУС

### API Endpoints - Формат данных:

| Endpoint | Формат | Примечание |
|----------|--------|-----------|
| `/api/auth/*` | camelCase | Новые endpoints |
| `/api/orders` (GET) | camelCase | Обновлен |
| `/api/orders/[id]` (GET) | camelCase | Новый |
| `/api/parts` (GET) | snake_case | Совместимость |
| `/api/parts/[id]` (GET) | snake_case | Совместимость |
| `/api/brands` | camelCase | Новый |
| `/api/warehouses` | camelCase | Новый |
| `/api/notifications` | camelCase | Новый |
| `/api/finance/*` | snake_case | Совместимость |
| `/api/crm/customers` | **оба формата** | Максимальная совместимость |
| `/api/analytics/*` | camelCase | Новые endpoints |

### Страницы - Используемый формат:

| Страница | Формат | Работает |
|----------|--------|----------|
| `/catalog` | snake_case & camelCase | ✅ |
| `/product/[id]` | snake_case & camelCase | ✅ |
| `/cart` | camelCase | ✅ |
| `/checkout` | camelCase | ✅ |
| `/admin/dashboard` | camelCase | ✅ |
| `/admin/orders` | camelCase | ✅ |
| `/admin/inventory` | snake_case | ✅ |
| `/admin/customers` | snake_case | ✅ |
| `/admin/finance` | snake_case | ✅ |
| `/admin/analytics` | camelCase | ✅ |

---

## 🎊 РЕЗУЛЬТАТ

**Все страницы работают:** ✅  
**Нет ошибок в консоли:** ✅  
**Формат данных:** ✅ Совместимый  
**Django зависимости:** ❌ Удалены  

**Проект использует смешанный подход для максимальной совместимости между старым Django API и новым SvelteKit API**

