<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { partsApi, cartUtils, seoApi, formatUtils } from '$lib/utils/api.js';
  import { goto } from '$app/navigation';
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
  const maxQuantity = $derived(Math.min(part?.available || 0, 10)); // Ограничение до 10 для примера

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
      // Сброс количества при загрузке нового товара
      quantity = 1;
    } catch (error) {
      console.error('Ошибка загрузки товара:', error);
      // Перенаправляем на 404 или страницу каталога, если товар не найден
      goto('/catalog', { replaceState: true });
    } finally {
      isLoading = false;
    }
  }

  // Загрузка похожих товаров
  async function loadSimilarParts() {
    if (!productId) return;

    try {
      // В реальном приложении здесь может быть более сложная логика
      // Например, запрос товаров того же бренда или категории, исключая текущий
      const allParts = await partsApi.getParts({ page_size: 8 }); // Загружаем несколько товаров
      similarParts = (allParts.results || [])
        .filter(p => p.id !== part.id) // Исключаем текущий товар
        .slice(0, 4); // Берем первые 4
    } catch (error) {
      console.error('Ошибка загрузки похожих товаров:', error);
    }
  }

  // Загрузка SEO метаданных
  async function loadSeoMeta() {
    if (!productId) return;
    try {
      // Предполагаем, что slug для страницы товара может быть 'product-detail'
      // или динамически генерироваться из ID/названия
      seoMeta = await seoApi.getSeoMeta(`product-${productId}`);
    } catch (error) {
      console.error('Ошибка загрузки SEO метаданных:', error);
      seoMeta = null; // Сбросить, если не найдено
    }
  }

  // Эффект для загрузки данных при изменении productId
  $effect(() => {
    if (productId) {
      loadPart();
      loadSimilarParts();
      loadSeoMeta();
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
                onclick={() => selectImage(index)}
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
          <div class="text-3xl font-bold text-primary-500 mb-2">{formatUtils.formatPrice(part.price_opt)}</div>
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
                  onclick={() => changeQuantity(-1)}
                  disabled={quantity <= 1}
                  class="px-3 py-2 hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  -
                </button>
                <span class="px-4 py-2 border-x border-neutral-300">{quantity}</span>
                <button
                  onclick={() => changeQuantity(1)}
                  disabled={quantity >= maxQuantity}
                  class="px-3 py-2 hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  +
                </button>
              </div>
            </div>
          </div>

          <button
            onclick={handleAddToCart}
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
                  <span class="font-bold text-primary-500">{formatUtils.formatPrice(similarPart.price_opt)}</span>
                  <span class="text-xs text-neutral-500">{similarPart.available} шт.</span>
                </div>
                <button
                  onclick={(e) => { e.preventDefault(); goto(`/product/${similarPart.id}`); }}
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