<script>
  // Пропсы компонента (Svelte 5 синтаксис)
  import { createEventDispatcher } from 'svelte';
  import { formatUtils, imageUtils } from '$lib/utils/api.js';
  let {
    part,
    showWarehouse = false,
    compact = false
  } = $props();
  
  // Реактивное состояние
  let isImageLoading = $state(true);
  let imageError = $state(false);
  const dispatch = createEventDispatcher();
  
  // Производные значения
  let hasImage = $derived(part.main_image?.url);
  let imageUrl = $derived(imageUtils.getAbsoluteUrl(part.main_image?.url));
  let isInStock = $derived(part.available > 0);
  let stockStatus = $derived(
    part.available === 0 ? 'Нет в наличии' :
    part.available <= 5 ? 'Мало на складе' :
    'В наличии'
  );
  let stockStatusClass = $derived(
    part.available === 0 ? 'bg-red-100 text-red-800' :
    part.available <= 5 ? 'badge-accent' :
    'badge-success'
  );
  
  // Обработчики
  function handleImageLoad() {
    isImageLoading = false;
  }
  
  function handleImageError() {
    isImageLoading = false;
    imageError = true;
  }
  
  function handleAddToCart(event) {
    event.preventDefault();
    event.stopPropagation();
    if (!isInStock) return;
    dispatch('addToCart', { part });
  }
</script>

<a href="/product/{part.id}" class="card-hover group block {compact ? 'p-4' : 'p-6'}">
  <!-- Изображение товара -->
  <div class="aspect-square bg-gradient-to-br from-secondary-50 to-secondary-100 rounded-xl mb-6 flex items-center justify-center overflow-hidden relative">
    {#if hasImage && !imageError}
      <img 
        src={imageUrl} 
        alt={part.main_image.alt || part.title}
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
        onload={handleImageLoad}
        onerror={handleImageError}
      />
      {#if isImageLoading}
        <div class="absolute inset-0 bg-gradient-to-br from-secondary-100 to-secondary-200 animate-pulse rounded-xl"></div>
      {/if}
    {:else}
      <div class="text-center">
        <svg class="text-secondary-400 mx-auto mb-2 {compact ? 'w-12 h-12' : 'w-16 h-16'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="text-xs text-secondary-500">Изображение</p>
      </div>
    {/if}
    
    <!-- Статус наличия -->
    <div class="absolute top-3 right-3">
      <span class="badge {stockStatusClass}">
        {stockStatus}
      </span>
    </div>
  </div>
  
  <!-- Информация о товаре -->
  <div class="space-y-4">
    <div>
      <h3 class="font-bold text-secondary-900 line-clamp-2 group-hover:text-primary-600 transition-colors text-lg leading-tight">
        {part.title}
      </h3>
      
      <div class="flex items-center justify-between mt-2">
        <span class="text-sm font-medium text-primary-600 bg-primary-50 px-2 py-1 rounded-lg">
          {part.brand_name}
        </span>
        {#if showWarehouse}
          <span class="text-xs text-secondary-500 bg-secondary-100 px-2 py-1 rounded-lg">
            {part.warehouse_name}
          </span>
        {/if}
      </div>
    </div>
    
    <!-- Номера товара -->
    {#if part.original_number || part.manufacturer_number}
      <div class="space-y-2">
        {#if part.original_number}
          <div class="text-xs text-secondary-600 bg-secondary-50 px-3 py-2 rounded-lg">
            <span class="font-medium text-secondary-700">Оригинал:</span> {part.original_number}
          </div>
        {/if}
        {#if part.manufacturer_number}
          <div class="text-xs text-secondary-600 bg-secondary-50 px-3 py-2 rounded-lg">
            <span class="font-medium text-secondary-700">Производитель:</span> {part.manufacturer_number}
          </div>
        {/if}
      </div>
    {/if}
    
    <!-- Цена и кнопка -->
    <div class="space-y-4">
      <div class="text-center">
        <div class="text-2xl font-bold text-gradient mb-1">
          {part.price_opt ? formatUtils.formatPrice(Number(part.price_opt)) : 'Цена по запросу'}
        </div>
        {#if part.available > 0}
          <div class="text-sm text-secondary-500">
            Остаток: <span class="font-medium text-secondary-700">{part.available} шт.</span>
          </div>
        {/if}
      </div>
      
      <button
        onclick={handleAddToCart}
        disabled={!isInStock}
        class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
      >
        {#if isInStock}
          <img src="/icons/shoping_cart.png" alt="В корзину" class="w-4 h-4 mr-2 object-contain icon-white" />
          В корзину
        {:else}
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Нет в наличии
        {/if}
      </button>
    </div>
  </div>
</a>