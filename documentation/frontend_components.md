# Компоненты каталога и карточки товара

## 🧩 Компоненты

### PartCard.svelte

Карточка товара для отображения в каталоге.

#### Пропсы:
- `part` (Object) - объект товара
- `showWarehouse` (Boolean) - показывать ли склад (по умолчанию: false)
- `compact` (Boolean) - компактный режим (по умолчанию: false)

#### События:
- `addToCart` - событие добавления в корзину

#### Пример использования:

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
  showWarehouse={true}
  on:addToCart={handleAddToCart}
/>
```

#### Особенности:
- Автоматическое определение статуса наличия
- Адаптивное изображение с fallback
- Hover эффекты и анимации
- Поддержка мобильных устройств

### CatalogFilters.svelte

Компонент фильтров для каталога товаров.

#### Пропсы:
- `brands` (Array) - список брендов
- `warehouses` (Array) - список складов
- `filters` (Object) - текущие фильтры
- `onFilterChange` (Function) - обработчик изменения фильтров
- `onClearFilters` (Function) - обработчик сброса фильтров

#### Пример использования:

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

#### Особенности:
- Адаптивный дизайн с мобильным меню
- Активные фильтры с возможностью удаления
- Валидация полей ввода
- Sticky позиционирование

### Pagination.svelte

Компонент пагинации для навигации по страницам.

#### Пропсы:
- `currentPage` (Number) - текущая страница
- `totalPages` (Number) - общее количество страниц
- `onPageChange` (Function) - обработчик смены страницы

#### Пример использования:

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

#### Особенности:
- Умная пагинация с многоточием
- Адаптивные кнопки навигации
- Поддержка клавиатуры
- Accessibility атрибуты

## 📄 Страницы

### Каталог (/catalog/+page.svelte)

Страница каталога товаров с фильтрами и пагинацией.

#### Функциональность:
- Загрузка товаров из API
- Фильтрация по различным параметрам
- Сортировка товаров
- Пагинация
- Добавление в корзину
- Адаптивная сетка товаров

#### Состояние:
```javascript
let parts = $state([]);
let brands = $state([]);
let warehouses = $state([]);
let isLoading = $state(true);
let currentPage = $state(1);
let totalPages = $state(1);
let totalCount = $state(0);
let filters = $state({
  search: '',
  brand: '',
  warehouse: '',
  price_min: '',
  price_max: '',
  in_stock: false,
  ordering: '-created_at'
});
```

#### API интеграция:
```javascript
// Загрузка товаров
async function loadParts() {
  const params = {
    page: currentPage,
    page_size: 12,
    ...filters
  };
  
  const data = await partsApi.getParts(params);
  parts = data.results || [];
  totalPages = Math.ceil(data.count / 12);
  totalCount = data.count;
}

// Загрузка справочников
async function loadReferences() {
  const [brandsData, warehousesData] = await Promise.all([
    brandsApi.getBrands(),
    warehousesApi.getWarehouses()
  ]);
  
  brands = brandsData.results || brandsData;
  warehouses = warehousesData.results || warehousesData;
}
```

### Страница товара (/product/[id]/+page.svelte)

Детальная страница товара с галереей изображений.

#### Функциональность:
- Загрузка детальной информации о товаре
- Галерея изображений с переключением
- Управление количеством для корзины
- Добавление в корзину
- Похожие товары
- SEO метатеги

#### Состояние:
```javascript
let part = $state(null);
let similarParts = $state([]);
let isLoading = $state(true);
let selectedImageIndex = $state(0);
let quantity = $state(1);
let isAddingToCart = $state(false);
```

#### API интеграция:
```javascript
// Загрузка товара
async function loadPart() {
  part = await partsApi.getPart(productId);
}

// Загрузка похожих товаров
async function loadSimilarParts() {
  similarParts = await partsApi.getSimilarParts(productId);
}

// Добавление в корзину
async function addToCart() {
  cartUtils.addToCart(part, quantity);
}
```

## 🔧 Утилиты

### API клиент (api.js)

Централизованный клиент для работы с API.

#### Основные методы:

```javascript
// Товары
const parts = await partsApi.getParts(params);
const part = await partsApi.getPart(id);
const similar = await partsApi.getSimilarParts(id);

// Справочники
const brands = await brandsApi.getBrands();
const warehouses = await warehousesApi.getWarehouses();

// SEO
const meta = await seoApi.getPageMeta(slug);
const settings = await seoApi.getSettings();
```

#### Корзина:

```javascript
// Добавить товар
cartUtils.addToCart(part, quantity);

// Обновить количество
cartUtils.updateQuantity(partId, newQuantity);

// Удалить товар
cartUtils.removeFromCart(partId);

// Получить общую стоимость
const totalPrice = cartUtils.getTotalPrice();
```

#### Форматирование:

```javascript
// Форматирование цены
formatUtils.formatPrice(2500); // "2 500 ₽"

// Форматирование числа
formatUtils.formatNumber(1234567); // "1 234 567"

// Форматирование даты
formatUtils.formatDate('2024-01-15'); // "15 января 2024 г."
```

## 🎨 Стилизация

### CSS классы

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

/* Сетка товаров */
.products-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

/* Фильтры */
.filters-sidebar {
  @apply lg:w-80;
}

.filters-content {
  @apply space-y-6;
}

/* Пагинация */
.pagination-nav {
  @apply flex items-center justify-center space-x-1;
}

.pagination-button {
  @apply btn-outline disabled:opacity-50 disabled:cursor-not-allowed;
}

.pagination-button.active {
  @apply btn-primary;
}
```

### Адаптивность

```css
/* Мобильные устройства */
@media (max-width: 768px) {
  .products-grid {
    @apply grid-cols-1 gap-4;
  }
  
  .filters-sidebar {
    @apply w-full;
  }
  
  .filters-content {
    @apply hidden;
  }
  
  .filters-content.expanded {
    @apply block;
  }
}

/* Планшеты */
@media (min-width: 768px) and (max-width: 1024px) {
  .products-grid {
    @apply grid-cols-2 gap-6;
  }
}

/* Десктоп */
@media (min-width: 1024px) {
  .products-grid {
    @apply grid-cols-3 gap-6;
  }
}
```

## 🚀 Производительность

### Оптимизации

1. **Ленивая загрузка изображений:**
```svelte
<img 
  src={image.url} 
  alt={image.alt}
  loading="lazy"
  class="w-full h-full object-cover"
/>
```

2. **Виртуализация для больших списков:**
```javascript
// Для списков с большим количеством товаров
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

3. **Кэширование API запросов:**
```javascript
// Простое кэширование в памяти
const cache = new Map();

async function getCachedData(key, fetcher) {
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const data = await fetcher();
  cache.set(key, data);
  return data;
}
```

4. **Debounce для поиска:**
```javascript
import { debounce } from 'lodash-es';

const debouncedSearch = debounce((query) => {
  // Выполнить поиск
}, 300);
```

## 🔍 SEO оптимизация

### Метатеги

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

## 🧪 Тестирование

### Unit тесты

```javascript
// Тест компонента PartCard
import { render } from '@testing-library/svelte';
import PartCard from '$lib/components/PartCard.svelte';

test('renders part card with correct information', () => {
  const part = {
    id: 1,
    title: 'Test Part',
    brand_name: 'Test Brand',
    price_opt: 1000,
    available: 5
  };
  
  const { getByText } = render(PartCard, { part });
  
  expect(getByText('Test Part')).toBeInTheDocument();
  expect(getByText('Test Brand')).toBeInTheDocument();
  expect(getByText('1 000 ₽')).toBeInTheDocument();
});
```

### E2E тесты

```javascript
// Тест каталога
test('catalog page loads and filters work', async ({ page }) => {
  await page.goto('/catalog');
  
  // Проверяем загрузку товаров
  await expect(page.locator('.part-card')).toBeVisible();
  
  // Тестируем фильтры
  await page.fill('input[placeholder*="Поиск"]', 'тормозные');
  await page.click('button[type="submit"]');
  
  // Проверяем результаты
  await expect(page.locator('.part-card')).toBeVisible();
});
```

## 📱 Мобильная оптимизация

### Touch события

```svelte
<!-- Swipe для галереи изображений -->
<div 
  class="image-gallery"
  on:touchstart={handleTouchStart}
  on:touchmove={handleTouchMove}
  on:touchend={handleTouchEnd}
>
  <!-- Изображения -->
</div>
```

### Адаптивные изображения

```svelte
<picture>
  <source media="(min-width: 1024px)" srcset={image.large} />
  <source media="(min-width: 768px)" srcset={image.medium} />
  <img src={image.small} alt={image.alt} />
</picture>
```

### Мобильное меню фильтров

```svelte
<!-- Мобильное меню фильтров -->
<div class="md:hidden">
  <button on:click={toggleFilters} class="btn-outline w-full">
    Фильтры
  </button>
  
  {#if showFilters}
    <div class="filters-mobile">
      <!-- Фильтры -->
    </div>
  {/if}
</div>
```





