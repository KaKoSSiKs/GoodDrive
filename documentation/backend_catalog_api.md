# Примеры API ответов для каталога автозапчастей GoodDrive

## 1. GET /api/parts/ - Список автозапчастей

### Запрос:
```
GET /api/parts/?brand=1&price_min=100&price_max=1000&in_stock=true&page=1
```

### Ответ:
```json
{
    "count": 150,
    "next": "http://localhost:8000/api/parts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "is_active": true,
            "title": "Тормозные колодки передние",
            "label": "BRAKE_PAD_FRONT",
            "original_number": "123456789",
            "manufacturer_number": "BP001",
            "brand_name": "Brembo",
            "warehouse_name": "Склад №1",
            "quantity": 50,
            "stock": 45,
            "reserve": 5,
            "available": 40,
            "price_opt": 2500.00,
            "main_image": {
                "url": "https://example.com/images/brake_pad_1.jpg",
                "alt": "Тормозные колодки Brembo"
            },
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "is_active": true,
            "title": "Масляный фильтр",
            "label": "OIL_FILTER",
            "original_number": "987654321",
            "manufacturer_number": "OF002",
            "brand_name": "Mann-Filter",
            "warehouse_name": "Склад №2",
            "quantity": 100,
            "stock": 95,
            "reserve": 10,
            "available": 85,
            "price_opt": 450.00,
            "main_image": {
                "url": "https://example.com/images/oil_filter_1.jpg",
                "alt": "Масляный фильтр Mann-Filter"
            },
            "created_at": "2024-01-14T14:20:00Z"
        }
    ]
}
```

## 2. GET /api/parts/{id}/ - Детальная информация об автозапчасти

### Запрос:
```
GET /api/parts/1/
```

### Ответ:
```json
{
    "id": 1,
    "is_active": true,
    "title": "Тормозные колодки передние",
    "label": "BRAKE_PAD_FRONT",
    "original_number": "123456789",
    "manufacturer_number": "BP001",
    "brand": {
        "id": 1,
        "name": "Brembo",
        "country": "Италия",
        "site": "https://www.brembo.com",
        "parts_count": 25
    },
    "warehouse": {
        "id": 1,
        "name": "Склад №1",
        "address": "ул. Промышленная, 15, Москва",
        "parts_count": 120
    },
    "quantity": 50,
    "stock": 45,
    "reserve": 5,
    "available": 40,
    "price_opt": 2500.00,
    "description": "Высококачественные тормозные колодки для передних колес. Обеспечивают отличное торможение и долгий срок службы.",
    "images": [
        {
            "id": 1,
            "image_url": "https://example.com/images/brake_pad_1.jpg",
            "alt_text": "Тормозные колодки Brembo - вид спереди",
            "order_index": 1
        },
        {
            "id": 2,
            "image_url": "https://example.com/images/brake_pad_2.jpg",
            "alt_text": "Тормозные колодки Brembo - вид сбоку",
            "order_index": 2
        }
    ],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T16:45:00Z"
}
```

## 3. GET /api/parts/available/ - Только доступные автозапчасти

### Запрос:
```
GET /api/parts/available/?brand_name=Brembo
```

### Ответ:
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "is_active": true,
            "title": "Тормозные колодки передние",
            "label": "BRAKE_PAD_FRONT",
            "original_number": "123456789",
            "manufacturer_number": "BP001",
            "brand_name": "Brembo",
            "warehouse_name": "Склад №1",
            "quantity": 50,
            "stock": 45,
            "reserve": 5,
            "available": 40,
            "price_opt": 2500.00,
            "main_image": {
                "url": "https://example.com/images/brake_pad_1.jpg",
                "alt": "Тормозные колодки Brembo"
            },
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

## 4. GET /api/parts/low_stock/ - Автозапчасти с низким остатком

### Запрос:
```
GET /api/parts/low_stock/
```

### Ответ:
```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 15,
            "is_active": true,
            "title": "Свечи зажигания",
            "label": "SPARK_PLUG",
            "original_number": "555666777",
            "manufacturer_number": "SP003",
            "brand_name": "NGK",
            "warehouse_name": "Склад №1",
            "quantity": 10,
            "stock": 8,
            "reserve": 3,
            "available": 5,
            "price_opt": 350.00,
            "main_image": {
                "url": "https://example.com/images/spark_plug_1.jpg",
                "alt": "Свечи зажигания NGK"
            },
            "created_at": "2024-01-10T09:15:00Z"
        }
    ]
}
```

## 5. GET /api/parts/{id}/similar/ - Похожие автозапчасти

### Запрос:
```
GET /api/parts/1/similar/
```

### Ответ:
```json
[
    {
        "id": 3,
        "is_active": true,
        "title": "Тормозные диски передние",
        "label": "BRAKE_DISC_FRONT",
        "original_number": "111222333",
        "manufacturer_number": "BD001",
        "brand_name": "Brembo",
        "warehouse_name": "Склад №1",
        "quantity": 30,
        "stock": 25,
        "reserve": 3,
        "available": 22,
        "price_opt": 4500.00,
        "main_image": {
            "url": "https://example.com/images/brake_disc_1.jpg",
            "alt": "Тормозные диски Brembo"
        },
        "created_at": "2024-01-12T11:20:00Z"
    }
]
```

## 6. GET /api/brands/ - Список брендов

### Запрос:
```
GET /api/brands/
```

### Ответ:
```json
[
    {
        "id": 1,
        "name": "Brembo",
        "country": "Италия",
        "site": "https://www.brembo.com",
        "parts_count": 25
    },
    {
        "id": 2,
        "name": "Mann-Filter",
        "country": "Германия",
        "site": "https://www.mann-filter.com",
        "parts_count": 18
    }
]
```

## 7. GET /api/warehouses/ - Список складов

### Запрос:
```
GET /api/warehouses/
```

### Ответ:
```json
[
    {
        "id": 1,
        "name": "Склад №1",
        "address": "ул. Промышленная, 15, Москва",
        "parts_count": 120
    },
    {
        "id": 2,
        "name": "Склад №2",
        "address": "пр. Автомобильный, 42, Санкт-Петербург",
        "parts_count": 85
    }
]
```

## Доступные фильтры для /api/parts/:

- `brand` - ID бренда
- `brand_name` - Название бренда (частичное совпадение)
- `warehouse` - ID склада
- `warehouse_name` - Название склада (частичное совпадение)
- `price_min` - Минимальная цена
- `price_max` - Максимальная цена
- `available_min` - Минимальное доступное количество
- `available_max` - Максимальное доступное количество
- `in_stock` - Только в наличии (true/false)
- `is_active` - Только активные (true/false)
- `original_number` - Оригинальный номер (частичное совпадение)
- `manufacturer_number` - Номер производителя (частичное совпадение)
- `created_after` - Создано после даты (YYYY-MM-DD)
- `created_before` - Создано до даты (YYYY-MM-DD)
- `search` - Поиск по названию, описанию, номерам
- `show_inactive` - Показать неактивные (true/false)

## Сортировка:
- `ordering` - Поля для сортировки: title, price_opt, available, created_at, updated_at
- По умолчанию: сортировка по дате создания (новые сначала)





