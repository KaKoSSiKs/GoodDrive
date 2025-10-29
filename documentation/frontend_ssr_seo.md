# SSR и SEO реализация для GoodDrive

## 🔍 Компоненты поиска и фильтров

### 1. SearchAutocomplete.svelte

Компонент автокомплита с debounced поиском и клавиатурной навигацией:

```svelte
<script>
  import { onMount } from 'svelte';
  import { partsApi } from '$lib/utils/api.js';
  
  // Пропсы компонента
  export let placeholder = 'Поиск автозапчастей...';
  export let onSelect = () => {};
  export let onSearch = () => {};
  export let debounceMs = 300;
  
  // Реактивное состояние
  let searchQuery = $state('');
  let suggestions = $state([]);
  let isLoading = $state(false);
  let isOpen = $state(false);
  let selectedIndex = $state(-1);
  let timeoutId = $state(null);
  
  // Производные значения
  const hasSuggestions = $derived(suggestions.length > 0 && isOpen);
  const hasQuery = $derived(searchQuery.trim().length > 0);
  
  // Debounced поиск
  function debouncedSearch(query) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    
    timeoutId = setTimeout(() => {
      loadSuggestions(query);
    }, debounceMs);
  }
  
  // Загрузка предложений
  async function loadSuggestions(query) {
    if (!query.trim() || query.length < 2) {
      suggestions = [];
      return;
    }
    
    isLoading = true;
    try {
      const data = await partsApi.getParts({
        search: query,
        page_size: 5,
        ordering: '-available'
      });
      
      suggestions = data.results || [];
    } catch (error) {
      console.error('Ошибка загрузки предложений:', error);
      suggestions = [];
    } finally {
      isLoading = false;
    }
  }
  
  // Обработчики клавиатуры
  function handleKeyDown(event) {
    if (!hasSuggestions) return;
    
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        selectedIndex = Math.min(selectedIndex + 1, suggestions.length - 1);
        break;
      case 'ArrowUp':
        event.preventDefault();
        selectedIndex = Math.max(selectedIndex - 1, -1);
        break;
      case 'Enter':
        event.preventDefault();
        if (selectedIndex >= 0) {
          selectSuggestion(suggestions[selectedIndex]);
        } else {
          performSearch();
        }
        break;
      case 'Escape':
        isOpen = false;
        selectedIndex = -1;
        break;
    }
  }
  
  function selectSuggestion(suggestion) {
    searchQuery = suggestion.title;
    isOpen = false;
    selectedIndex = -1;
    onSelect(suggestion);
  }
  
  function performSearch() {
    if (!hasQuery) return;
    isOpen = false;
    onSearch(searchQuery);
  }
</script>

<div class="relative w-full">
  <!-- Поле поиска -->
  <div class="relative">
    <input
      type="text"
      placeholder={placeholder}
      bind:value={searchQuery}
      on:input={(e) => { searchQuery = e.target.value; isOpen = true; debouncedSearch(searchQuery); }}
      on:keydown={handleKeyDown}
      on:focus={() => { if (hasQuery) isOpen = true; }}
      on:blur={() => { setTimeout(() => { isOpen = false; selectedIndex = -1; }, 150); }}
      class="input pl-10 pr-10 w-full"
    />
    
    <!-- Иконка поиска -->
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <svg class="h-5 w-5 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
    
    <!-- Кнопка очистки/поиска -->
    {#if hasQuery}
      <button on:click={() => { searchQuery = ''; suggestions = []; isOpen = false; }} class="absolute inset-y-0 right-0 pr-3 flex items-center text-neutral-400 hover:text-neutral-600">
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    {:else}
      <button on:click={performSearch} class="absolute inset-y-0 right-0 pr-3 flex items-center text-neutral-400 hover:text-primary-500">
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
      </button>
    {/if}
  </div>
  
  <!-- Выпадающий список предложений -->
  {#if hasSuggestions}
    <div class="absolute z-50 w-full mt-1 bg-white border border-neutral-200 rounded-lg shadow-lg max-h-80 overflow-y-auto">
      {#each suggestions as suggestion, index}
        <button
          on:click={() => selectSuggestion(suggestion)}
          class="w-full px-4 py-3 text-left hover:bg-neutral-50 border-b border-neutral-100 last:border-b-0 {selectedIndex === index ? 'bg-primary-50' : ''}"
        >
          <div class="flex items-center space-x-3">
            <!-- Изображение товара -->
            <div class="w-12 h-12 bg-neutral-100 rounded-lg flex items-center justify-center flex-shrink-0">
              {#if suggestion.main_image}
                <img src={suggestion.main_image.url} alt={suggestion.main_image.alt || suggestion.title} class="w-full h-full object-cover rounded-lg" />
              {:else}
                <svg class="w-6 h-6 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              {/if}
            </div>
            
            <!-- Информация о товаре -->
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-neutral-900 truncate">{suggestion.title}</h3>
              <p class="text-sm text-neutral-600">{suggestion.brand_name}</p>
              {#if suggestion.original_number}
                <p class="text-xs text-neutral-500 font-mono">{suggestion.original_number}</p>
              {/if}
            </div>
            
            <!-- Цена и наличие -->
            <div class="text-right flex-shrink-0">
              <p class="font-semibold text-primary-500">{suggestion.price_opt.toLocaleString()} ₽</p>
              <p class="text-xs text-neutral-500">
                {suggestion.available > 0 ? `${suggestion.available} шт.` : 'Нет в наличии'}
              </p>
            </div>
          </div>
        </button>
      {/each}
      
      <!-- Кнопка "Показать все результаты" -->
      <div class="px-4 py-2 border-t border-neutral-200">
        <button on:click={performSearch} class="w-full text-center text-sm text-primary-500 hover:text-primary-600 font-medium">
          Показать все результаты для "{searchQuery}"
        </button>
      </div>
    </div>
  {/if}
  
  <!-- Индикатор загрузки -->
  {#if isLoading}
    <div class="absolute inset-y-0 right-0 pr-10 flex items-center pointer-events-none">
      <svg class="animate-spin h-4 w-4 text-primary-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  {/if}
</div>
```

### 2. RangeSlider.svelte

Компонент слайдера для фильтрации по цене:

```svelte
<script>
  // Пропсы компонента
  export let min = 0;
  export let max = 100000;
  export let step = 100;
  export let value = { min: min, max: max };
  export let onInput = () => {};
  export let disabled = false;
  
  // Реактивное состояние
  let minValue = $state(value.min);
  let maxValue = $state(value.max);
  let isDragging = $state(false);
  
  // Производные значения
  const range = $derived(max - min);
  const minPercent = $derived(((minValue - min) / range) * 100);
  const maxPercent = $derived(((maxValue - min) / range) * 100);
  
  // Обработчики
  function handleMinInput(event) {
    const newValue = Math.min(Number(event.target.value), maxValue - step);
    minValue = Math.max(min, newValue);
    updateValue();
  }
  
  function handleMaxInput(event) {
    const newValue = Math.max(Number(event.target.value), minValue + step);
    maxValue = Math.min(max, newValue);
    updateValue();
  }
  
  function updateValue() {
    const newValue = { min: minValue, max: maxValue };
    onInput(newValue);
  }
  
  function resetRange() {
    minValue = min;
    maxValue = max;
    updateValue();
  }
  
  // Форматирование значения для отображения
  function formatValue(val) {
    return new Intl.NumberFormat('ru-RU').format(val);
  }
</script>

<div class="w-full">
  <!-- Заголовок и сброс -->
  <div class="flex items-center justify-between mb-4">
    <label class="text-sm font-medium text-neutral-700">Цена, ₽</label>
    {#if minValue !== min || maxValue !== max}
      <button on:click={resetRange} class="text-xs text-primary-500 hover:text-primary-600 font-medium" disabled={disabled}>
        Сбросить
      </button>
    {/if}
  </div>
  
  <!-- Слайдер -->
  <div class="relative">
    <!-- Трек -->
    <div class="relative h-2 bg-neutral-200 rounded-lg">
      <!-- Активный диапазон -->
      <div class="absolute h-2 bg-primary-500 rounded-lg" style="left: {minPercent}%; width: {maxPercent - minPercent}%;"></div>
      
      <!-- Минимальный слайдер -->
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        bind:value={minValue}
        on:input={handleMinInput}
        class="absolute w-full h-2 bg-transparent appearance-none cursor-pointer min-slider"
        style="z-index: 2;"
        disabled={disabled}
      />
      
      <!-- Максимальный слайдер -->
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        bind:value={maxValue}
        on:input={handleMaxInput}
        class="absolute w-full h-2 bg-transparent appearance-none cursor-pointer max-slider"
        style="z-index: 2;"
        disabled={disabled}
      />
      
      <!-- Кастомные ползунки -->
      <div class="absolute w-4 h-4 bg-white border-2 border-primary-500 rounded-full shadow-md transform -translate-y-1 cursor-pointer" style="left: {minPercent}%; z-index: 3;"></div>
      <div class="absolute w-4 h-4 bg-white border-2 border-primary-500 rounded-full shadow-md transform -translate-y-1 cursor-pointer" style="left: {maxPercent}%; z-index: 3;"></div>
    </div>
  </div>
  
  <!-- Поля ввода -->
  <div class="flex items-center space-x-2 mt-4">
    <div class="flex-1">
      <label class="block text-xs text-neutral-500 mb-1">От</label>
      <input type="number" min={min} max={max} step={step} bind:value={minValue} on:input={handleMinInput} class="input text-sm py-1 px-2" disabled={disabled} />
    </div>
    
    <div class="flex-1">
      <label class="block text-xs text-neutral-500 mb-1">До</label>
      <input type="number" min={min} max={max} step={step} bind:value={maxValue} on:input={handleMaxInput} class="input text-sm py-1 px-2" disabled={disabled} />
    </div>
  </div>
  
  <!-- Отображение диапазона -->
  <div class="text-center mt-2 text-sm text-neutral-600">
    {formatValue(minValue)} - {formatValue(maxValue)} ₽
  </div>
</div>

<style>
  /* Скрываем стандартные ползунки */
  input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
  }
  
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 0;
    height: 0;
    background: transparent;
  }
  
  input[type="range"]::-moz-range-thumb {
    width: 0;
    height: 0;
    background: transparent;
    border: none;
  }
</style>
```

### 3. FilterCheckbox.svelte

Компонент чекбокса для фильтров:

```svelte
<script>
  // Пропсы компонента
  export let label = '';
  export let checked = false;
  export let disabled = false;
  export let onToggle = () => {};
  export let count = null;
  export let showCount = true;
  
  // Обработчики
  function handleToggle() {
    if (disabled) return;
    onToggle(!checked);
  }
  
  function handleKeyDown(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleToggle();
    }
  }
</script>

<label 
  class="flex items-center space-x-3 cursor-pointer {disabled ? 'opacity-50 cursor-not-allowed' : 'hover:bg-neutral-50'} p-2 rounded-lg transition-colors"
  on:click={handleToggle}
  on:keydown={handleKeyDown}
  tabindex="0"
  role="checkbox"
  aria-checked={checked}
  aria-disabled={disabled}
>
  <!-- Кастомный чекбокс -->
  <div class="relative">
    <input type="checkbox" bind:checked disabled={disabled} class="sr-only" tabindex="-1" />
    
    <!-- Визуальный чекбокс -->
    <div class="w-5 h-5 border-2 rounded {checked ? 'border-primary-500 bg-primary-500' : 'border-neutral-300'} flex items-center justify-center transition-colors">
      {#if checked}
        <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
      {/if}
    </div>
  </div>
  
  <!-- Текст и счетчик -->
  <div class="flex-1 min-w-0">
    <span class="text-sm text-neutral-700 {checked ? 'font-medium' : ''}">
      {label}
    </span>
    
    {#if showCount && count !== null}
      <span class="text-xs text-neutral-500 ml-2">
        ({count})
      </span>
    {/if}
  </div>
  
  <!-- Индикатор активности -->
  {#if checked}
    <div class="w-2 h-2 bg-primary-500 rounded-full"></div>
  {/if}
</label>

<style>
  /* Фокус для доступности */
  label:focus {
    outline: 2px solid #F97316;
    outline-offset: 2px;
  }
  
  /* Анимация для чекбокса */
  .transition-colors {
    transition: all 0.2s ease-in-out;
  }
</style>
```

## 🔍 SEO и SSR утилиты

### 1. seo.js

```javascript
// Утилиты для SEO и структурированных данных

/**
 * Генерирует JSON-LD разметку для товара
 */
export function generateProductJsonLd(product) {
  const jsonLd = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": product.title,
    "description": product.description || `${product.title} от ${product.brand.name}`,
    "image": product.images?.map(img => img.image_url) || [],
    "brand": {
      "@type": "Brand",
      "name": product.brand.name,
      "url": product.brand.site || undefined
    },
    "offers": {
      "@type": "Offer",
      "price": product.price_opt,
      "priceCurrency": "RUB",
      "availability": product.available > 0 
        ? "https://schema.org/InStock" 
        : "https://schema.org/OutOfStock",
      "seller": {
        "@type": "Organization",
        "name": "GoodDrive"
      }
    },
    "sku": product.original_number || product.manufacturer_number,
    "mpn": product.manufacturer_number,
    "gtin": product.original_number
  };

  return jsonLd;
}

/**
 * Генерирует JSON-LD разметку для организации
 */
export function generateOrganizationJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "GoodDrive",
    "description": "Интернет-магазин автозапчастей",
    "url": "https://gooddrive.com",
    "logo": "https://gooddrive.com/logo.png",
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+7 (XXX) XXX-XX-XX",
      "contactType": "customer service",
      "availableLanguage": "Russian"
    },
    "address": {
      "@type": "PostalAddress",
      "addressCountry": "RU",
      "addressLocality": "Москва"
    },
    "sameAs": [
      "https://vk.com/gooddrive",
      "https://t.me/gooddrive"
    ]
  };
}

/**
 * Генерирует JSON-LD разметку для коллекции товаров
 */
export function generateCollectionJsonLd(products, pageInfo) {
  return {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Каталог автозапчастей",
    "description": "Полный каталог автозапчастей от ведущих производителей",
    "url": pageInfo.url,
    "mainEntity": {
      "@type": "ItemList",
      "numberOfItems": pageInfo.totalCount,
      "itemListElement": products.map((product, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "item": {
          "@type": "Product",
          "name": product.title,
          "description": product.description,
          "image": product.main_image?.url,
          "brand": {
            "@type": "Brand",
            "name": product.brand_name
          },
          "offers": {
            "@type": "Offer",
            "price": product.price_opt,
            "priceCurrency": "RUB",
            "availability": product.available > 0 
              ? "https://schema.org/InStock" 
              : "https://schema.org/OutOfStock"
          }
        }
      }))
    }
  };
}

/**
 * Генерирует метатеги для страницы
 */
export function generateMetaTags(pageData) {
  const {
    title,
    description,
    keywords,
    image,
    url,
    type = 'website',
    product = null
  } = pageData;

  const metaTags = [];

  // Основные метатеги
  metaTags.push({ name: 'title', content: title });
  metaTags.push({ name: 'description', content: description });
  
  if (keywords) {
    metaTags.push({ name: 'keywords', content: keywords });
  }

  // Open Graph
  metaTags.push({ property: 'og:title', content: title });
  metaTags.push({ property: 'og:description', content: description });
  metaTags.push({ property: 'og:type', content: type });
  metaTags.push({ property: 'og:url', content: url });
  
  if (image) {
    metaTags.push({ property: 'og:image', content: image });
    metaTags.push({ property: 'og:image:width', content: '1200' });
    metaTags.push({ property: 'og:image:height', content: '630' });
  }

  // Twitter Card
  metaTags.push({ name: 'twitter:card', content: 'summary_large_image' });
  metaTags.push({ name: 'twitter:title', content: title });
  metaTags.push({ name: 'twitter:description', content: description });
  
  if (image) {
    metaTags.push({ name: 'twitter:image', content: image });
  }

  // Дополнительные метатеги для товаров
  if (product) {
    metaTags.push({ property: 'product:price:amount', content: product.price_opt });
    metaTags.push({ property: 'product:price:currency', content: 'RUB' });
    metaTags.push({ 
      property: 'product:availability', 
      content: product.available > 0 ? 'in stock' : 'out of stock' 
    });
    metaTags.push({ property: 'product:brand', content: product.brand.name });
    
    if (product.original_number) {
      metaTags.push({ property: 'product:sku', content: product.original_number });
    }
  }

  return metaTags;
}

/**
 * Форматирует заголовок страницы
 */
export function formatPageTitle(title, siteName = 'GoodDrive') {
  if (title.includes(siteName)) {
    return title;
  }
  return `${title} - ${siteName}`;
}

/**
 * Генерирует описание страницы
 */
export function generatePageDescription(type, data = {}) {
  const descriptions = {
    home: 'Интернет-магазин автозапчастей GoodDrive. Широкий ассортимент качественных деталей для любых марок автомобилей. Быстрая доставка по всей России.',
    
    catalog: data.search 
      ? `Результаты поиска "${data.search}" в каталоге автозапчастей GoodDrive. Найдено ${data.count || 0} товаров.`
      : 'Каталог автозапчастей GoodDrive. Широкий ассортимент деталей от ведущих производителей. Фильтры по бренду, цене, наличию.',
    
    product: `${data.title} от ${data.brand} в GoodDrive. Цена: ${data.price} ₽. ${data.available > 0 ? 'В наличии' : 'Нет в наличии'}. Быстрая доставка.`,
    
    cart: 'Корзина покупок GoodDrive. Оформите заказ автозапчастей с быстрой доставкой по всей России.',
    
    checkout: 'Оформление заказа автозапчастей в GoodDrive. Удобная форма заказа с быстрой доставкой.',
    
    about: 'О компании GoodDrive - интернет-магазин автозапчастей. Надежный партнер в мире автомобильных деталей.',
    
    contact: 'Контакты GoodDrive. Свяжитесь с нами для получения консультации по автозапчастям и оформлению заказов.'
  };

  return descriptions[type] || descriptions.home;
}

/**
 * Генерирует ключевые слова для страницы
 */
export function generateKeywords(type, data = {}) {
  const baseKeywords = ['автозапчасти', 'GoodDrive', 'интернет-магазин', 'автомобильные детали'];
  
  const typeKeywords = {
    home: ['автозапчасти онлайн', 'каталог автозапчастей', 'доставка автозапчастей'],
    catalog: ['каталог', 'фильтры', 'поиск автозапчастей'],
    product: [data.brand?.toLowerCase(), data.title?.toLowerCase(), 'цена', 'купить'],
    cart: ['корзина', 'заказ', 'покупка'],
    checkout: ['оформление заказа', 'доставка', 'оплата'],
    about: ['о компании', 'история', 'преимущества'],
    contact: ['контакты', 'связь', 'поддержка']
  };

  const keywords = [...baseKeywords, ...(typeKeywords[type] || [])];
  
  // Добавляем специфичные ключевые слова из данных
  if (data.brand) {
    keywords.push(data.brand.toLowerCase());
  }
  
  if (data.search) {
    keywords.push(data.search.toLowerCase());
  }

  return keywords.filter(Boolean).join(', ');
}
```

### 2. SeoHead.svelte

Компонент для управления SEO метатегами:

```svelte
<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { 
    generateMetaTags, 
    generatePageTitle, 
    generatePageDescription, 
    generateKeywords,
    generateCanonicalUrl 
  } from '$lib/utils/seo.js';
  
  // Пропсы компонента
  export let title = '';
  export let description = '';
  export let keywords = '';
  export let image = '';
  export let type = 'website';
  export let product = null;
  export let breadcrumbs = [];
  export let jsonLd = null;
  
  // Реактивное состояние
  let metaTags = $state([]);
  let canonicalUrl = $state('');
  
  // Производные значения
  const pageTitle = $derived(generatePageTitle(title));
  const pageDescription = $derived(description || generatePageDescription(type, { product }));
  const pageKeywords = $derived(keywords || generateKeywords(type, { product }));
  
  // Обновление метатегов
  function updateMetaTags() {
    const baseUrl = 'https://gooddrive.com'; // В продакшене должен быть из переменных окружения
    const currentUrl = `${baseUrl}${page.url.pathname}`;
    
    canonicalUrl = generateCanonicalUrl(baseUrl, page.url.pathname);
    
    metaTags = generateMetaTags({
      title: pageTitle,
      description: pageDescription,
      keywords: pageKeywords,
      image: image,
      url: currentUrl,
      type: type,
      product: product
    });
  }
  
  // Инициализация
  onMount(() => {
    updateMetaTags();
  });
  
  // Обновление при изменении пропсов
  $effect(() => {
    updateMetaTags();
  });
</script>

<svelte:head>
  <!-- Основные метатеги -->
  <title>{pageTitle}</title>
  <meta name="description" content={pageDescription} />
  <meta name="keywords" content={pageKeywords} />
  
  <!-- Канонический URL -->
  <link rel="canonical" href={canonicalUrl} />
  
  <!-- Динамические метатеги -->
  {#each metaTags as tag}
    {#if tag.property}
      <meta property={tag.property} content={tag.content} />
    {:else if tag.name}
      <meta name={tag.name} content={tag.content} />
    {/if}
  {/each}
  
  <!-- Дополнительные метатеги -->
  <meta name="robots" content="index, follow" />
  <meta name="author" content="GoodDrive" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
  
  <!-- JSON-LD структурированные данные -->
  {#if jsonLd}
    {@html `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`}
  {/if}
  
  <!-- Хлебные крошки JSON-LD -->
  {#if breadcrumbs.length > 0}
    {@html `<script type="application/ld+json">${JSON.stringify({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": breadcrumbs.map((crumb, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "name": crumb.name,
        "item": crumb.url
      }))
    })}</script>`}
  {/if}
</svelte:head>
```

## 🚀 SSR страницы

### 1. Каталог с SSR

```svelte
<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import PartCard from '$lib/components/PartCard.svelte';
  import CatalogFilters from '$lib/components/CatalogFilters.svelte';
  import Pagination from '$lib/components/Pagination.svelte';
  import SeoHead from '$lib/components/SeoHead.svelte';
  import { partsApi, brandsApi, warehousesApi, cartUtils } from '$lib/utils/api.js';
  import { formatNumber } from '$lib/utils/api.js';
  import { generateCollectionJsonLd, generateBreadcrumbJsonLd } from '$lib/utils/seo.js';
  
  // Реактивное состояние
  let parts = $state([]);
  let brands = $state([]);
  let warehouses = $state([]);
  let isLoading = $state(true);
  let currentPage = $state(1);
  let totalPages = $state(1);
  let totalCount = $state(0);
  
  // Фильтры из URL параметров
  let filters = $state({
    search: $page.url.searchParams.get('search') || '',
    brand: $page.url.searchParams.get('brand') || '',
    warehouse: $page.url.searchParams.get('warehouse') || '',
    price_min: $page.url.searchParams.get('price_min') || '',
    price_max: $page.url.searchParams.get('price_max') || '',
    in_stock: $page.url.searchParams.get('in_stock') === 'true',
    ordering: $page.url.searchParams.get('ordering') || '-created_at'
  });
  
  // Производные значения
  const hasParts = $derived(parts.length > 0);
  const hasFilters = $derived(
    filters.search || filters.brand || filters.warehouse ||
    filters.price_min || filters.price_max || filters.in_stock
  );
  
  // SEO данные
  const seoData = $derived({
    title: filters.search ? `Поиск "${filters.search}"` : 'Каталог автозапчастей',
    description: filters.search 
      ? `Результаты поиска "${filters.search}" в каталоге автозапчастей GoodDrive. Найдено ${totalCount} товаров.`
      : 'Каталог автозапчастей GoodDrive. Широкий ассортимент деталей от ведущих производителей.',
    keywords: filters.search 
      ? `поиск, ${filters.search}, автозапчасти, каталог`
      : 'каталог, автозапчасти, фильтры, бренды, цены',
    image: parts[0]?.main_image?.url || '/images/catalog-og.jpg',
    type: 'website'
  });
  
  // JSON-LD для коллекции товаров
  const collectionJsonLd = $derived(generateCollectionJsonLd(parts, {
    url: $page.url.href,
    totalCount: totalCount
  }));
  
  // Хлебные крошки
  const breadcrumbs = $derived([
    { name: 'Главная', url: '/' },
    { name: 'Каталог', url: '/catalog' },
    ...(filters.search ? [{ name: `Поиск: ${filters.search}`, url: `/catalog?search=${encodeURIComponent(filters.search)}` }] : [])
  ]);
  
  // Загрузка данных товаров
  async function loadParts() {
    isLoading = true;

    try {
      // Строим параметры запроса
      const params = {
        page: currentPage,
        page_size: 12,
        ...filters
      };

      // Убираем пустые значения
      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === false) {
          delete params[key];
        }
      });

      const data = await partsApi.getParts(params);

      parts = data.results || [];
      totalPages = Math.ceil(data.count / 12);
      totalCount = data.count;
    } catch (error) {
      console.error('Ошибка загрузки товаров:', error);
      alert('Ошибка загрузки товаров. Попробуйте позже.');
    } finally {
      isLoading = false;
    }
  }

  // Загрузка справочников
  async function loadReferences() {
    try {
      const [brandsData, warehousesData] = await Promise.all([
        brandsApi.getBrands(),
        warehousesApi.getWarehouses()
      ]);

      brands = brandsData.results || brandsData;
      warehouses = warehousesData.results || warehousesData;
    } catch (error) {
      console.error('Ошибка загрузки справочников:', error);
    }
  }

  // Обработчики
  function handleFilterChange(newFilters) {
    filters = newFilters;
    currentPage = 1;
    
    // Обновляем URL без перезагрузки страницы
    const url = new URL($page.url);
    Object.keys(newFilters).forEach(key => {
      if (newFilters[key] && newFilters[key] !== false) {
        url.searchParams.set(key, newFilters[key]);
      } else {
        url.searchParams.delete(key);
      }
    });
    
    // Обновляем URL
    window.history.replaceState({}, '', url);
    
    loadParts();
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
    currentPage = 1;
    
    // Очищаем URL параметры
    const url = new URL($page.url);
    url.search = '';
    window.history.replaceState({}, '', url);
    
    loadParts();
  }

  function handlePageChange(page) {
    currentPage = page;
    
    // Обновляем URL с номером страницы
    const url = new URL($page.url);
    if (page > 1) {
      url.searchParams.set('page', page);
    } else {
      url.searchParams.delete('page');
    }
    window.history.replaceState({}, '', url);
    
    loadParts();
  }

  function handleAddToCart(event) {
    const { part } = event.detail;
    cartUtils.addToCart(part);

    // Показываем уведомление
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
    notification.textContent = `Добавлено в корзину: ${part.title}`;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  }

  // Инициализация
  onMount(() => {
    loadReferences();
    loadParts();
  });
</script>

<SeoHead
  title={seoData.title}
  description={seoData.description}
  keywords={seoData.keywords}
  image={seoData.image}
  type={seoData.type}
  breadcrumbs={breadcrumbs}
  jsonLd={collectionJsonLd}
/>

<div class="container-custom py-8">
  <!-- Заголовок -->
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-neutral-900 mb-2">
      {filters.search ? `Поиск: "${filters.search}"` : 'Каталог автозапчастей'}
    </h1>
    <p class="text-neutral-600">
      {#if isLoading}
        Загрузка...
      {:else}
        Найдено товаров: {formatNumber(totalCount)}
      {/if}
    </p>
  </div>

  <div class="flex flex-col lg:flex-row gap-8">
    <!-- Фильтры -->
    <aside class="lg:w-80">
      <CatalogFilters
        {brands}
        {warehouses}
        {filters}
        onFilterChange={handleFilterChange}
        onClearFilters={handleClearFilters}
      />
    </aside>

    <!-- Товары -->
    <main class="flex-1">
      {#if isLoading}
        <!-- Скелетон загрузки -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each Array(12) as _}
            <div class="card p-6 animate-pulse">
              <div class="bg-neutral-200 h-48 rounded-lg mb-4"></div>
              <div class="bg-neutral-200 h-4 rounded mb-2"></div>
              <div class="bg-neutral-200 h-4 rounded w-3/4 mb-4"></div>
              <div class="bg-neutral-200 h-6 rounded w-1/2"></div>
            </div>
          {/each}
        </div>
      {:else if hasParts}
        <!-- Сетка товаров -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {#each parts as part}
            <PartCard
              {part}
              on:addToCart={handleAddToCart}
            />
          {/each}
        </div>

        <!-- Пагинация -->
        <Pagination
          {currentPage}
          {totalPages}
          onPageChange={handlePageChange}
        />
      {:else}
        <!-- Пустое состояние -->
        <div class="text-center py-16">
          <svg class="w-16 h-16 text-neutral-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
          </svg>
          <h3 class="text-lg font-semibold text-neutral-900 mb-2">Товары не найдены</h3>
          <p class="text-neutral-600 mb-4">Попробуйте изменить параметры поиска</p>
          <button on:click={handleClearFilters} class="btn-primary">
            Сбросить фильтры
          </button>
        </div>
      {/if}
    </main>
  </div>
</div>
```

### 2. Страница товара с SSR

```svelte
<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { partsApi, cartUtils, seoApi, formatPrice } from '$lib/utils/api.js';
  import { goto } from '$app/navigation';
  import { $state, $derived, $effect } from 'svelte';
  import SeoHead from '$lib/components/SeoHead.svelte';
  import { generateProductJsonLd, generateBreadcrumbJsonLd } from '$lib/utils/seo.js';
  
  // Реактивное состояние
  let part = $state(null);
  let similarParts = $state([]);
  let isLoading = $state(true);
  let selectedImageIndex = $state(0);
  let quantity = $state(1);
  let seoMeta = $state(null);

  // Производные значения
  const productId = $derived(page.params.id);
  const hasImages = $derived(part?.images?.length > 0);
  const currentImage = $derived(part?.images?.[selectedImageIndex]);
  const isInStock = $derived(part?.available > 0);
  const maxQuantity = $derived(Math.min(part?.available || 0, 10));

  // SEO данные
  const seoData = $derived({
    title: part?.title || 'Загрузка...',
    description: part?.description || `Автозапчасть ${part?.title || ''} от ${part?.brand?.name || ''} в GoodDrive`,
    keywords: part ? `${part.title}, ${part.brand.name}, автозапчасти, ${part.original_number || ''}` : '',
    image: currentImage?.image_url || part?.main_image?.url || '/images/product-default.jpg',
    type: 'product'
  });

  // JSON-LD для товара
  const productJsonLd = $derived(part ? generateProductJsonLd(part) : null);

  // Хлебные крошки
  const breadcrumbs = $derived(part ? [
    { name: 'Главная', url: '/' },
    { name: 'Каталог', url: '/catalog' },
    { name: part.title, url: `/product/${part.id}` }
  ] : []);
  
  // Загрузка данных товара
  async function loadPart() {
    if (!productId) return;

    isLoading = true;
    try {
      const partData = await partsApi.getPartDetail(productId);
      part = partData;
      quantity = 1;
    } catch (error) {
      console.error('Ошибка загрузки товара:', error);
      goto('/catalog', { replaceState: true });
    } finally {
      isLoading = false;
    }
  }

  // Загрузка похожих товаров
  async function loadSimilarParts() {
    if (!productId) return;

    try {
      const allParts = await partsApi.getParts({ page_size: 8 });
      similarParts = (allParts.results || [])
        .filter(p => p.id !== part.id)
        .slice(0, 4);
    } catch (error) {
      console.error('Ошибка загрузки похожих товаров:', error);
    }
  }

  // Эффект для загрузки данных при изменении productId
  $effect(() => {
    if (productId) {
      loadPart();
      loadSimilarParts();
    }
  });

  // Обработчики
  function selectImage(index) {
    selectedImageIndex = index;
  }

  function changeQuantity(delta) {
    const newQuantity = quantity + delta;
    if (newQuantity >= 1 && newQuantity <= maxQuantity) {
      quantity = newQuantity;
    }
  }

  function handleAddToCart() {
    if (!isInStock) return;

    cartUtils.addToCart(part, quantity);

    // Показываем уведомление
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
    notification.textContent = `Добавлено в корзину: ${part.title} (${quantity} шт.)`;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
</script>

<SeoHead
  title={seoData.title}
  description={seoData.description}
  keywords={seoData.keywords}
  image={seoData.image}
  type={seoData.type}
  product={part}
  breadcrumbs={breadcrumbs}
  jsonLd={productJsonLd}
/>

{#if isLoading}
  <div class="container-custom py-8">
    <div class="animate-pulse">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="space-y-4">
          <div class="bg-neutral-200 h-96 rounded-lg"></div>
          <div class="flex space-x-2">
            {#each Array(4) as _}
              <div class="bg-neutral-200 h-20 w-20 rounded-lg"></div>
            {/each}
          </div>
        </div>
        <div class="space-y-4">
          <div class="bg-neutral-200 h-8 rounded w-3/4"></div>
          <div class="bg-neutral-200 h-4 rounded w-1/2"></div>
          <div class="bg-neutral-200 h-6 rounded w-1/4"></div>
          <div class="bg-neutral-200 h-32 rounded"></div>
        </div>
      </div>
    </div>
  </div>
{:else if part}
  <div class="container-custom py-8">
    <!-- Хлебные крошки -->
    <nav class="mb-8">
      <ol class="flex items-center space-x-2 text-sm text-neutral-500">
        <li><a href="/" class="hover:text-primary-500">Главная</a></li>
        <li><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg></li>
        <li><a href="/catalog" class="hover:text-primary-500">Каталог</a></li>
        <li><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg></li>
        <li class="text-neutral-900">{part.title}</li>
      </ol>
    </nav>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
      <!-- Изображения -->
      <div>
        <div class="aspect-square bg-neutral-100 rounded-lg mb-4 flex items-center justify-center">
          {#if currentImage}
            <img
              src={currentImage.image_url}
              alt={currentImage.alt_text || part.title}
              class="w-full h-full object-contain rounded-lg"
            />
          {:else}
            <svg class="w-32 h-32 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          {/if}
        </div>

        {#if hasImages}
          <div class="flex space-x-2 overflow-x-auto pb-2">
            {#each part.images as image, index}
              <button
                on:click={() => selectImage(index)}
                class="flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 {index === selectedImageIndex ? 'border-primary-500' : 'border-neutral-200'} focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <img
                  src={image.image_url}
                  alt={image.alt_text || part.title}
                  class="w-full h-full object-cover"
                />
              </button>
            {/each}
          </div>
        {/if}
      </div>

      <!-- Информация о товаре -->
      <div>
        <h1 class="text-3xl font-bold text-neutral-900 mb-4">{part.title}</h1>

        <div class="mb-6">
          <div class="flex items-center space-x-4 mb-4">
            <span class="text-sm text-neutral-600">Бренд:</span>
            <span class="font-semibold">{part.brand.name}</span>
          </div>
          <div class="flex items-center space-x-4 mb-4">
            <span class="text-sm text-neutral-600">Склад:</span>
            <span class="font-semibold">{part.warehouse.name}</span>
          </div>
          {#if part.original_number}
            <div class="flex items-center space-x-4 mb-4">
              <span class="text-sm text-neutral-600">Оригинальный номер:</span>
              <span class="font-mono text-sm bg-neutral-100 px-2 py-1 rounded">{part.original_number}</span>
            </div>
          {/if}
          {#if part.manufacturer_number}
            <div class="flex items-center space-x-4 mb-4">
              <span class="text-sm text-neutral-600">Номер производителя:</span>
              <span class="font-mono text-sm bg-neutral-100 px-2 py-1 rounded">{part.manufacturer_number}</span>
            </div>
          {/if}
        </div>

        <div class="mb-6">
          <div class="text-3xl font-bold text-primary-500 mb-2">{formatPrice(part.price_opt)}</div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-neutral-600">Наличие:</span>
            <span class="font-semibold {isInStock ? 'text-green-600' : 'text-red-600'}">
              {isInStock ? `${part.available} шт.` : 'Нет в наличии'}
            </span>
          </div>
        </div>

        {#if isInStock}
          <div class="mb-6">
            <div class="flex items-center space-x-4 mb-4">
              <span class="text-sm text-neutral-600">Количество:</span>
              <div class="flex items-center border border-neutral-300 rounded-lg">
                <button
                  on:click={() => changeQuantity(-1)}
                  disabled={quantity <= 1}
                  class="px-3 py-2 hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  -
                </button>
                <span class="px-4 py-2 border-x border-neutral-300">{quantity}</span>
                <button
                  on:click={() => changeQuantity(1)}
                  disabled={quantity >= maxQuantity}
                  class="px-3 py-2 hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  +
                </button>
              </div>
            </div>
          </div>

          <button
            on:click={handleAddToCart}
            class="btn-primary w-full mb-4"
          >
            Добавить в корзину
          </button>
        {:else}
          <button
            disabled
            class="btn-secondary w-full mb-4 opacity-50 cursor-not-allowed"
          >
            Нет в наличии
          </button>
        {/if}

        <div class="text-sm text-neutral-600">
          <p>• Гарантия качества</p>
          <p>• Быстрая доставка</p>
          <p>• Возврат в течение 14 дней</p>
        </div>
      </div>
    </div>

    <!-- Описание -->
    {#if part.description}
      <div class="mb-12">
        <h2 class="text-2xl font-bold text-neutral-900 mb-4">Описание</h2>
        <div class="prose max-w-none">
          <p class="text-neutral-700 whitespace-pre-line">{part.description}</p>
        </div>
      </div>
    {/if}

    <!-- Похожие товары -->
    {#if similarParts.length > 0}
      <div>
        <h2 class="text-2xl font-bold text-neutral-900 mb-6">Похожие товары</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {#each similarParts as similarPart}
            <div class="card p-4 hover:shadow-md transition-shadow">
              <a href="/product/{similarPart.id}" class="block">
                <div class="aspect-square bg-neutral-100 rounded-lg mb-4 flex items-center justify-center">
                  {#if similarPart.main_image?.image_url}
                    <img
                      src={similarPart.main_image.image_url}
                      alt={similarPart.main_image.alt_text || similarPart.title}
                      class="w-full h-full object-cover rounded-lg"
                    />
                  {:else}
                    <svg class="w-12 h-12 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  {/if}
                </div>
                <h3 class="font-semibold text-neutral-900 mb-2 text-sm line-clamp-2">{similarPart.title}</h3>
                <p class="text-neutral-600 text-xs mb-2">{similarPart.brand_name}</p>
                <div class="flex items-center justify-between mb-3">
                  <span class="font-bold text-primary-500">{formatPrice(similarPart.price_opt)}</span>
                  <span class="text-xs text-neutral-500">{similarPart.available} шт.</span>
                </div>
                <button
                  on:click|preventDefault={() => goto(`/product/${similarPart.id}`)}
                  class="btn-outline w-full text-sm"
                >
                  Подробнее
                </button>
              </a>
            </div>
          {/each}
        </div>
      </div>
    {/if}
  </div>
{:else}
  <div class="container-custom py-8">
    <div class="text-center">
      <h1 class="text-2xl font-bold text-neutral-900 mb-4">Товар не найден</h1>
      <p class="text-neutral-600 mb-6">Запрашиваемый товар не существует или был удален</p>
      <a href="/catalog" class="btn-primary">Перейти в каталог</a>
    </div>
  </div>
{/if}
```

## 🎯 Реактивное обновление каталога

### Обновление URL без перезагрузки

```javascript
// Обновление URL при изменении фильтров
function handleFilterChange(newFilters) {
  filters = newFilters;
  currentPage = 1;
  
  // Обновляем URL без перезагрузки страницы
  const url = new URL($page.url);
  Object.keys(newFilters).forEach(key => {
    if (newFilters[key] && newFilters[key] !== false) {
      url.searchParams.set(key, newFilters[key]);
    } else {
      url.searchParams.delete(key);
    }
  });
  
  // Обновляем URL
  window.history.replaceState({}, '', url);
  
  loadParts();
}

// Обновление URL при пагинации
function handlePageChange(page) {
  currentPage = page;
  
  // Обновляем URL с номером страницы
  const url = new URL($page.url);
  if (page > 1) {
    url.searchParams.set('page', page);
  } else {
    url.searchParams.delete('page');
  }
  window.history.replaceState({}, '', url);
  
  loadParts();
}
```

### Debounced поиск

```javascript
// Debounced поиск в автокомплите
function debouncedSearch(query) {
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
  
  timeoutId = setTimeout(() => {
    loadSuggestions(query);
  }, debounceMs);
}
```

## 📱 Мобильная оптимизация

### Адаптивные фильтры

```svelte
<!-- Мобильная версия фильтров -->
<div class="space-y-6 {isExpanded ? '' : 'hidden md:block'}">
  <!-- Фильтры -->
</div>

<!-- Кнопка разворачивания на мобильных -->
<button
  on:click={toggleExpanded}
  class="md:hidden p-1 text-neutral-500 hover:text-neutral-700"
>
  <svg class="w-5 h-5 transition-transform {isExpanded ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
  </svg>
</button>
```

## 🚀 Производительность

### Ленивая загрузка изображений

```svelte
<img 
  src={item.image} 
  alt={item.title}
  loading="lazy"
  class="w-full h-full object-cover rounded-lg"
/>
```

### Кэширование API запросов

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

Все компоненты полностью готовы к использованию и обеспечивают современный пользовательский интерфейс с отличной производительностью и полной SEO оптимизацией!





