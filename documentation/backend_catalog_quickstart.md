# Быстрый старт работы с API каталога

## Создание базы данных

```bash
cd backend
python manage.py migrate
```

## Импорт данных из Excel

Сначала экспортируйте Excel в CSV:

1. Откройте `проваоваоао.xlsx` в Excel
2. Сохраните как CSV (разделители - запятые)
3. Назовите файл `parts.csv`
4. Положите в корень проекта (рядом с `manage.py`)

### Импорт первых 100 запчастей

```bash
python manage.py import_from_csv parts.csv --limit 100
```

### Импорт всех запчастей (6404 шт)

```bash
python manage.py import_from_csv parts.csv --limit 6500
```

## Запуск сервера

```bash
python manage.py runserver
```

## API Endpoints

### Каталог запчастей

#### Список всех запчастей
```http
GET /api/catalog/parts/
GET /api/catalog/parts/?page=1&page_size=12
```

#### Фильтрация по бренду
```http
GET /api/catalog/parts/?brand_name=Toyota
```

#### Фильтрация по цене
```http
GET /api/catalog/parts/?price_min=100&price_max=1000
```

#### Поиск
```http
GET /api/catalog/parts/?search=фильтр
```

#### Фильтр наличия
```http
GET /api/catalog/parts/?in_stock=true
```

#### Сортировка
```http
GET /api/catalog/parts/?ordering=price_opt
GET /api/catalog/parts/?ordering=-price_opt
```

### Детальная информация о запчасти
```http
GET /api/catalog/parts/{id}/
```

### Список брендов
```http
GET /api/catalog/brands/
```

### Список складов
```http
GET /api/catalog/warehouses/
```

## Примеры ответов API

### Список запчастей
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/catalog/parts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Фильтр масляный",
      "brand_name": "Toyota",
      "warehouse_name": "Основной склад",
      "price_opt": "350.00",
      "available": 15,
      "main_image": {
        "url": "https://via.placeholder.com/600x600?text=Auto+Part",
        "alt": "Фильтр масляный"
      }
    }
  ]
}
```

### Детальная информация
```json
{
  "id": 1,
  "title": "Фильтр масляный",
  "description": "Качественный масляный фильтр",
  "original_number": "04152-YZZA2",
  "manufacturer_number": "90915-YZZA2",
  "brand": {
    "id": 1,
    "name": "Toyota",
    "country": "Япония"
  },
  "warehouse": {
    "id": 1,
    "name": "Основной склад",
    "address": "г. Москва"
  },
  "price_opt": "350.00",
  "available": 15,
  "stock": 15,
  "reserve": 0,
  "images": [
    {
      "id": 1,
      "image_url": "https://via.placeholder.com/600x600?text=Auto+Part",
      "alt_text": "Фильтр масляный",
      "order_index": 0
    }
  ]
}
```

## Работа с корзиной

Корзина реализована на фронтенде через localStorage. Утилиты находятся в:
`frontend/src/lib/utils/api.js`

Методы:
- `cartUtils.addToCart(part, quantity)` - добавить в корзину
- `cartUtils.removeFromCart(partId)` - удалить из корзины
- `cartUtils.updateQuantity(partId, quantity)` - обновить количество
- `cartUtils.getCart()` - получить корзину
- `cartUtils.clearCart()` - очистить корзину

## Работа с заказами

После заполнения корзины, пользователь оформляет заказ через:
```http
POST /api/orders/
```

Тело запроса:
```json
{
  "customer_name": "Иван Иванов",
  "customer_phone": "+79991234567",
  "customer_email": "user@example.com",
  "delivery_address": "ул. Примерная, д. 1",
  "delivery_city": "Москва",
  "delivery_postal_code": "123456",
  "notes": "Комментарии к заказу",
  "items": [
    {
      "part_id": 1,
      "quantity": 2
    }
  ]
}
```
