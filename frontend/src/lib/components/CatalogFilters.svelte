<script>
  import FilterCheckbox from './FilterCheckbox.svelte';
  import RangeSlider from './RangeSlider.svelte';
  
  // Пропсы компонента
  export let brands = [];
  export let warehouses = [];
  export let filters = {};
  export let onFilterChange = () => {};
  export let onClearFilters = () => {};
  
  // Реактивное состояние
  let isExpanded = $state(false);
  let priceRange = $state({ min: filters.price_min || 0, max: filters.price_max || 100000 });
  
  // Производные значения
  const hasActiveFilters = $derived(
    filters.search || filters.brand || filters.warehouse || 
    filters.price_min || filters.price_max || filters.in_stock
  );
  
  // Обработчики
  function handleInputChange(field, value) {
    onFilterChange({ ...filters, [field]: value });
  }
  
  function handleSearchSubmit(event) {
    event.preventDefault();
    onFilterChange({ ...filters, search: event.target.search.value });
  }
  
  function handlePriceRangeChange(range) {
    priceRange = range;
    onFilterChange({ 
      ...filters, 
      price_min: range.min > 0 ? range.min : '',
      price_max: range.max < 100000 ? range.max : ''
    });
  }
  
  function handleBrandToggle(brandId, checked) {
    const currentBrands = filters.brand ? filters.brand.split(',') : [];
    let newBrands;
    
    if (checked) {
      newBrands = [...currentBrands, brandId.toString()];
    } else {
      newBrands = currentBrands.filter(id => id !== brandId.toString());
    }
    
    onFilterChange({ 
      ...filters, 
      brand: newBrands.length > 0 ? newBrands.join(',') : ''
    });
  }
  
  function handleWarehouseToggle(warehouseId, checked) {
    const currentWarehouses = filters.warehouse ? filters.warehouse.split(',') : [];
    let newWarehouses;
    
    if (checked) {
      newWarehouses = [...currentWarehouses, warehouseId.toString()];
    } else {
      newWarehouses = currentWarehouses.filter(id => id !== warehouseId.toString());
    }
    
    onFilterChange({ 
      ...filters, 
      warehouse: newWarehouses.length > 0 ? newWarehouses.join(',') : ''
    });
  }
  
  function toggleExpanded() {
    isExpanded = !isExpanded;
  }
  
  // Проверка выбранности бренда/склада
  function isBrandSelected(brandId) {
    return filters.brand ? filters.brand.split(',').includes(brandId.toString()) : false;
  }
  
  function isWarehouseSelected(warehouseId) {
    return filters.warehouse ? filters.warehouse.split(',').includes(warehouseId.toString()) : false;
  }
</script>

<div class="card p-6 sticky top-24">
  <!-- Заголовок фильтров -->
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-lg font-semibold text-neutral-900">Фильтры</h2>
    <div class="flex items-center space-x-2">
      {#if hasActiveFilters}
        <button 
          on:click={onClearFilters}
          class="text-sm text-primary-500 hover:text-primary-600 font-medium"
        >
          Сбросить
        </button>
      {/if}
      <button
        on:click={toggleExpanded}
        class="md:hidden p-1 text-neutral-500 hover:text-neutral-700"
      >
        <svg class="w-5 h-5 transition-transform {isExpanded ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>
  </div>
  
  <!-- Фильтры -->
  <div class="space-y-6 {isExpanded ? '' : 'hidden md:block'}">
    <!-- Поиск -->
    <div>
      <label class="block text-sm font-medium text-neutral-700 mb-2">Поиск</label>
      <form on:submit={handleSearchSubmit}>
        <div class="relative">
          <input
            type="text"
            name="search"
            placeholder="Название, номер..."
            value={filters.search || ''}
            on:input={(e) => handleInputChange('search', e.target.value)}
            class="input pl-10"
          />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          {#if filters.search}
            <button
              type="button"
              on:click={() => handleInputChange('search', '')}
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-neutral-400 hover:text-neutral-600"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          {/if}
        </div>
      </form>
    </div>
    
    <!-- Цена -->
    <div>
      <RangeSlider
        min={0}
        max={100000}
        step={100}
        value={priceRange}
        onInput={handlePriceRangeChange}
      />
    </div>
    
    <!-- Бренды -->
    <div>
      <label class="block text-sm font-medium text-neutral-700 mb-3">Бренды</label>
      <div class="space-y-2 max-h-48 overflow-y-auto">
        {#each brands.slice(0, 10) as brand}
          <FilterCheckbox
            label={brand.name}
            checked={isBrandSelected(brand.id)}
            count={brand.parts_count}
            onToggle={(checked) => handleBrandToggle(brand.id, checked)}
          />
        {/each}
        
        {#if brands.length > 10}
          <div class="text-xs text-neutral-500 pt-2 border-t border-neutral-200">
            Показано 10 из {brands.length} брендов
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Склады -->
    <div>
      <label class="block text-sm font-medium text-neutral-700 mb-3">Склады</label>
      <div class="space-y-2">
        {#each warehouses as warehouse}
          <FilterCheckbox
            label={warehouse.name}
            checked={isWarehouseSelected(warehouse.id)}
            count={warehouse.parts_count}
            onToggle={(checked) => handleWarehouseToggle(warehouse.id, checked)}
          />
        {/each}
      </div>
    </div>
    
    <!-- Наличие -->
    <div>
      <FilterCheckbox
        label="Только в наличии"
        checked={filters.in_stock || false}
        onToggle={(checked) => handleInputChange('in_stock', checked)}
      />
    </div>
    
    <!-- Сортировка -->
    <div>
      <label class="block text-sm font-medium text-neutral-700 mb-2">Сортировка</label>
      <select 
        value={filters.ordering || '-created_at'} 
        on:change={(e) => handleInputChange('ordering', e.target.value)}
        class="input"
      >
        <option value="-created_at">Новинки</option>
        <option value="price_opt">Цена: по возрастанию</option>
        <option value="-price_opt">Цена: по убыванию</option>
        <option value="title">Название: А-Я</option>
        <option value="-title">Название: Я-А</option>
        <option value="-available">Наличие: больше</option>
        <option value="available">Наличие: меньше</option>
      </select>
    </div>
  </div>
  
  <!-- Активные фильтры (только на мобильных) -->
  {#if hasActiveFilters}
    <div class="mt-6 md:hidden">
      <div class="flex flex-wrap gap-2">
        {#if filters.search}
          <span class="inline-flex items-center px-2 py-1 text-xs bg-primary-100 text-primary-800 rounded">
            Поиск: {filters.search}
            <button
              on:click={() => handleInputChange('search', '')}
              class="ml-1 text-primary-600 hover:text-primary-800"
            >
              ×
            </button>
          </span>
        {/if}
        
        {#if filters.brand}
          {#each filters.brand.split(',') as brandId}
            {@const brand = brands.find(b => b.id == brandId)}
            {#if brand}
              <span class="inline-flex items-center px-2 py-1 text-xs bg-primary-100 text-primary-800 rounded">
                Бренд: {brand.name}
                <button
                  on:click={() => handleBrandToggle(brandId, false)}
                  class="ml-1 text-primary-600 hover:text-primary-800"
                >
                  ×
                </button>
              </span>
            {/if}
          {/each}
        {/if}
        
        {#if filters.in_stock}
          <span class="inline-flex items-center px-2 py-1 text-xs bg-primary-100 text-primary-800 rounded">
            В наличии
            <button
              on:click={() => handleInputChange('in_stock', false)}
              class="ml-1 text-primary-600 hover:text-primary-800"
            >
              ×
            </button>
          </span>
        {/if}
      </div>
    </div>
  {/if}
</div>