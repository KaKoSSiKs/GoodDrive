<script>
  // Пропсы компонента
  export let part;
  export let showWarehouse = false;
  export let compact = false;
  
  // Реактивное состояние
  let isImageLoading = $state(true);
  let imageError = $state(false);
  
  // Производные значения
  const hasImage = $derived(part.main_image?.url);
  const isInStock = $derived(part.available > 0);
  const stockStatus = $derived(
    part.available === 0 ? 'Нет в наличии' :
    part.available <= 5 ? 'Мало на складе' :
    'В наличии'
  );
  const stockStatusClass = $derived(
    part.available === 0 ? 'text-red-600' :
    part.available <= 5 ? 'text-yellow-600' :
    'text-green-600'
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
    
    // Создаем событие для добавления в корзину
    const customEvent = new CustomEvent('addToCart', {
      detail: { part },
      bubbles: true
    });
    event.target.dispatchEvent(customEvent);
  }
</script>

<div class="card p-{compact ? '4' : '6'} hover:shadow-md transition-all duration-200 group">
  <!-- Изображение товара -->
  <div class="aspect-square bg-neutral-100 rounded-lg mb-4 flex items-center justify-center overflow-hidden relative">
    {#if hasImage && !imageError}
      <img 
        src={part.main_image.url} 
        alt={part.main_image.alt || part.title}
        class="w-full h-full object-cover transition-transform duration-200 group-hover:scale-105"
        on:load={handleImageLoad}
        on:error={handleImageError}
      />
      {#if isImageLoading}
        <div class="absolute inset-0 bg-neutral-200 animate-pulse"></div>
      {/if}
    {:else}
      <svg class="w-{compact ? '12' : '16'} h-{compact ? '12' : '16'} text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    {/if}
    
    <!-- Статус наличия -->
    <div class="absolute top-2 right-2">
      <span class="px-2 py-1 text-xs font-medium rounded-full {stockStatusClass} bg-white shadow-sm">
        {stockStatus}
      </span>
    </div>
  </div>
  
  <!-- Информация о товаре -->
  <div class="space-y-2">
    <h3 class="font-semibold text-neutral-900 line-clamp-2 group-hover:text-primary-600 transition-colors">
      {part.title}
    </h3>
    
    <div class="flex items-center justify-between text-sm text-neutral-600">
      <span class="font-medium">{part.brand_name}</span>
      {#if showWarehouse}
        <span class="text-xs">{part.warehouse_name}</span>
      {/if}
    </div>
    
    <!-- Номера товара -->
    {#if part.original_number || part.manufacturer_number}
      <div class="space-y-1">
        {#if part.original_number}
          <div class="text-xs text-neutral-500">
            <span class="font-medium">Оригинал:</span> {part.original_number}
          </div>
        {/if}
        {#if part.manufacturer_number}
          <div class="text-xs text-neutral-500">
            <span class="font-medium">Производитель:</span> {part.manufacturer_number}
          </div>
        {/if}
      </div>
    {/if}
    
    <!-- Цена и количество -->
    <div class="flex items-center justify-between">
      <div class="text-lg font-bold text-primary-500">
        {part.price_opt.toLocaleString()} ₽
      </div>
      <div class="text-sm text-neutral-500">
        {part.available} шт.
      </div>
    </div>
    
    <!-- Кнопка добавления в корзину -->
    <button
      on:click={handleAddToCart}
      disabled={!isInStock}
      class="w-full btn {isInStock ? 'btn-primary' : 'btn-secondary opacity-50 cursor-not-allowed'}"
    >
      {#if isInStock}
        Добавить в корзину
      {:else}
        Нет в наличии
      {/if}
    </button>
    
    <!-- Ссылка на детальную страницу -->
    <a 
      href="/product/{part.id}" 
      class="block w-full btn-outline text-center"
    >
      Подробнее
    </a>
  </div>
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>

