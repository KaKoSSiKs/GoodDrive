# API Примеры для каталога и карточки товара

## 📋 Каталог товаров

### Получить список товаров с фильтрами

```javascript
// Базовый запрос
const response = await fetch('/api/parts/');
const data = await response.json();

// С фильтрами
const params = new URLSearchParams({
  search: 'тормозные колодки',
  brand: '1',
  warehouse: '2',
  price_min: '1000',
  price_max: '5000',
  in_stock: 'true',
  ordering: '-created_at',
  page: '1',
  page_size: '12'
});

const response = await fetch(`/api/parts/?${params}`);
const data = await response.json();
```

### Пример ответа каталога

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
      "label": "Оригинал",
      "original_number": "123456789",
      "manufacturer_number": "ABC123",
      "brand_name": "Bosch",
      "warehouse_name": "Склад №1",
      "available": 15,
      "price_opt": 2500.00,
      "main_image": {
        "id": 1,
        "image_url": "/media/parts/1/brake_pads.jpg",
        "alt_text": "Тормозные колодки",
        "order_index": 0
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## 🔍 Детальная информация о товаре

### Получить товар по ID

```javascript
const response = await fetch('/api/parts/1/');
const part = await response.json();
```

### Пример ответа детальной страницы

```json
{
  "id": 1,
  "is_active": true,
  "title": "Тормозные колодки передние",
  "label": "Оригинал",
  "original_number": "123456789",
  "manufacturer_number": "ABC123",
  "brand": {
    "id": 1,
    "name": "Bosch",
    "country": "Германия",
    "site": "https://www.bosch.com",
    "parts_count": 45
  },
  "warehouse": {
    "id": 1,
    "name": "Склад №1",
    "address": "ул. Промышленная, 15",
    "parts_count": 120
  },
  "quantity": 20,
  "stock": 18,
  "reserve": 3,
  "available": 15,
  "price_opt": 2500.00,
  "description": "Высококачественные тормозные колодки для передних колес. Обеспечивают отличное торможение и долгий срок службы.",
  "images": [
    {
      "id": 1,
      "image_url": "/media/parts/1/brake_pads_1.jpg",
      "alt_text": "Тормозные колодки - вид спереди",
      "order_index": 0
    },
    {
      "id": 2,
      "image_url": "/media/parts/1/brake_pads_2.jpg",
      "alt_text": "Тормозные колодки - вид сбоку",
      "order_index": 1
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## 🏷️ Справочники

### Получить список брендов

```javascript
const response = await fetch('/api/brands/');
const brands = await response.json();
```

### Получить список складов

```javascript
const response = await fetch('/api/warehouses/');
const warehouses = await response.json();
```

## 🔗 Похожие товары

### Получить похожие товары

```javascript
const response = await fetch('/api/parts/1/similar/');
const similarParts = await response.json();
```

## 🛒 Работа с корзиной

### Добавить товар в корзину (локально)

```javascript
import { cartUtils } from '$lib/utils/api.js';

// Добавить товар
const cart = cartUtils.addToCart(part, quantity);

// Обновить количество
const updatedCart = cartUtils.updateQuantity(partId, newQuantity);

// Удалить товар
const updatedCart = cartUtils.removeFromCart(partId);

// Получить общую стоимость
const totalPrice = cartUtils.getTotalPrice();

// Получить количество товаров
const totalItems = cartUtils.getTotalItems();
```

## 📱 Использование в компонентах

### Компонент карточки товара

```svelte
<script>
  import PartCard from '$lib/components/PartCard.svelte';
  
  let part = {
    id: 1,
    title: "Тормозные колодки",
    brand_name: "Bosch",
    warehouse_name: "Склад №1",
    available: 15,
    price_opt: 2500.00,
    main_image: {
      url: "/media/parts/1/brake_pads.jpg",
      alt: "Тормозные колодки"
    }
  };
  
  function handleAddToCart(event) {
    const { part } = event.detail;
    console.log('Добавлено в корзину:', part);
  }
</script>

<PartCard 
  {part}
  on:addToCart={handleAddToCart}
/>
```

### Компонент фильтров

```svelte
<script>
  import CatalogFilters from '$lib/components/CatalogFilters.svelte';
  
  let brands = [
    { id: 1, name: "Bosch" },
    { id: 2, name: "Continental" }
  ];
  
  let warehouses = [
    { id: 1, name: "Склад №1" },
    { id: 2, name: "Склад №2" }
  ];
  
  let filters = {
    search: '',
    brand: '',
    warehouse: '',
    price_min: '',
    price_max: '',
    in_stock: false,
    ordering: '-created_at'
  };
  
  function handleFilterChange(newFilters) {
    filters = newFilters;
    // Обновить список товаров
  }
  
  function handleClearFilters() {
    filters = {
      search: '',
      brand: '',
      warehouse: '',
      price_min: '',
      price_max: '',
      in_stock: false,
      ordering: '-created_at'
    };
  }
</script>

<CatalogFilters 
  {brands}
  {warehouses}
  {filters}
  onFilterChange={handleFilterChange}
  onClearFilters={handleClearFilters}
/>
```

### Компонент пагинации

```svelte
<script>
  import Pagination from '$lib/components/Pagination.svelte';
  
  let currentPage = 1;
  let totalPages = 10;
  
  function handlePageChange(page) {
    currentPage = page;
    // Загрузить новую страницу
  }
</script>

<Pagination 
  {currentPage}
  {totalPages}
  onPageChange={handlePageChange}
/>
```

## 🔧 Утилиты API

### Базовый API клиент

```javascript
import { partsApi, brandsApi, warehousesApi } from '$lib/utils/api.js';

// Получить товары
const parts = await partsApi.getParts({
  search: 'тормозные',
  brand: '1',
  page: 1,
  page_size: 12
});

// Получить товар по ID
const part = await partsApi.getPart(1);

// Получить похожие товары
const similar = await partsApi.getSimilarParts(1);

// Получить бренды
const brands = await brandsApi.getBrands();

// Получить склады
const warehouses = await warehousesApi.getWarehouses();
```

### Обработка ошибок

```javascript
try {
  const parts = await partsApi.getParts();
  // Обработка успешного ответа
} catch (error) {
  console.error('Ошибка загрузки товаров:', error);
  // Показать уведомление пользователю
}
```

## 📊 Фильтрация и сортировка

### Доступные фильтры

- `search` - поиск по названию и номерам
- `brand` - фильтр по бренду (ID)
- `warehouse` - фильтр по складу (ID)
- `price_min` - минимальная цена
- `price_max` - максимальная цена
- `in_stock` - только в наличии
- `ordering` - сортировка

### Варианты сортировки

- `-created_at` - новинки (по умолчанию)
- `price_opt` - цена по возрастанию
- `-price_opt` - цена по убыванию
- `title` - название А-Я
- `-title` - название Я-А
- `-available` - наличие по убыванию
- `available` - наличие по возрастанию

## 🎨 Стилизация

### CSS классы для карточек

```css
/* Карточка товара */
.part-card {
  @apply card p-6 hover:shadow-md transition-all duration-200;
}

/* Изображение товара */
.part-image {
  @apply aspect-square bg-neutral-100 rounded-lg mb-4 flex items-center justify-center overflow-hidden;
}

/* Статус наличия */
.stock-status {
  @apply px-2 py-1 text-xs font-medium rounded-full;
}

.stock-status.in-stock {
  @apply text-green-600 bg-white shadow-sm;
}

.stock-status.low-stock {
  @apply text-yellow-600 bg-white shadow-sm;
}

.stock-status.out-of-stock {
  @apply text-red-600 bg-white shadow-sm;
}
```

### Адаптивная сетка

```css
/* Сетка товаров */
.products-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

/* На мобильных устройствах */
@media (max-width: 768px) {
  .products-grid {
    @apply grid-cols-1 gap-4;
  }
}
```

## 🚀 Производительность

### Ленивая загрузка изображений

```svelte
<img 
  src={image.url} 
  alt={image.alt}
  loading="lazy"
  class="w-full h-full object-cover"
/>
```

### Виртуализация для больших списков

```javascript
// Для списков с большим количеством товаров
// можно использовать виртуализацию
import { VirtualList } from 'svelte-virtual-list';

<VirtualList
  items={parts}
  height={600}
  itemHeight={200}
  let:item={part}
>
  <PartCard {part} />
</VirtualList>
```

## 🔍 SEO оптимизация

### Метатеги для страницы товара

```svelte
<svelte:head>
  <title>{part.title} - GoodDrive</title>
  <meta name="description" content={part.description} />
  <meta property="og:title" content={part.title} />
  <meta property="og:description" content={part.description} />
  <meta property="og:image" content={part.images[0]?.image_url} />
  <meta property="og:type" content="product" />
  <meta property="product:price:amount" content={part.price_opt} />
  <meta property="product:price:currency" content="RUB" />
  <meta property="product:availability" content={part.available > 0 ? 'in stock' : 'out of stock'} />
</svelte:head>
```

### Структурированные данные

```svelte
<script>
  const structuredData = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": part.title,
    "description": part.description,
    "image": part.images.map(img => img.image_url),
    "brand": {
      "@type": "Brand",
      "name": part.brand.name
    },
    "offers": {
      "@type": "Offer",
      "price": part.price_opt,
      "priceCurrency": "RUB",
      "availability": part.available > 0 ? "https://schema.org/InStock" : "https://schema.org/OutOfStock"
    }
  };
</script>

<svelte:head>
  <script type="application/ld+json">
    {JSON.stringify(structuredData)}
  </script>
</svelte:head>
```





