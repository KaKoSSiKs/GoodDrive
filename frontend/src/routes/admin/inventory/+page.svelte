<script>
  import { onMount } from 'svelte';
  import { partsApi, formatUtils, brandsApi, warehousesApi } from '$lib/utils/api.js';
  import ProductEditModal from '$lib/components/admin/ProductEditModal.svelte';
  import AddProductModal from '$lib/components/admin/AddProductModal.svelte';
  
  let parts = $state([]);
  let brands = $state([]);
  let warehouses = $state([]);
  let isLoading = $state(true);
  let selectedPart = $state(null);
  let isModalOpen = $state(false);
  let isAddModalOpen = $state(false);
  
  let filters = $state({
    search: '',
    stock_filter: 'all', // all, low, out
    brand: '',
    warehouse: ''
  });
  
  const stockFilterOptions = [
    { value: 'all', label: 'Все товары' },
    { value: 'low', label: 'Низкий остаток (≤5)' },
    { value: 'out', label: 'Нет в наличии' }
  ];
  
  async function loadParts() {
    try {
      isLoading = true;
      const params = {
        ordering: 'available',
        page_size: 100
      };
      
      if (filters.search) params.search = filters.search;
      if (filters.brand) params.brand = filters.brand;
      if (filters.warehouse) params.warehouse = filters.warehouse;
      
      let response;
      if (filters.stock_filter === 'low') {
        response = await partsApi.getLowStockParts(params);
      } else if (filters.stock_filter === 'out') {
        params.available_max = 0;
        response = await partsApi.getParts(params);
      } else {
        response = await partsApi.getParts(params);
      }
      
      parts = response.results || [];
    } catch (error) {
      console.error('Ошибка загрузки товаров:', error);
    } finally {
      isLoading = false;
    }
  }
  
  async function loadReferences() {
    try {
      const [brandsData, warehousesData] = await Promise.all([
        brandsApi.getBrands({ page_size: 100 }),
        warehousesApi.getWarehouses({ page_size: 100 })
      ]);
      
      brands = brandsData.results || brandsData;
      warehouses = warehousesData.results || warehousesData;
    } catch (error) {
      console.error('Ошибка загрузки справочников:', error);
    }
  }
  
  function handleFilterChange() {
    loadParts();
  }
  
  function handlePartClick(part) {
    selectedPart = part;
    isModalOpen = true;
  }
  
  function handleModalClose() {
    isModalOpen = false;
    selectedPart = null;
  }
  
  function handlePartUpdate() {
    loadParts();
  }
  
  function handleAddProduct() {
    isAddModalOpen = true;
  }
  
  function handleAddModalClose() {
    isAddModalOpen = false;
  }
  
  function handleProductAdded() {
    loadParts();
  }
  
  // Экспорт в CSV
  async function exportToCSV() {
    try {
      // Формируем CSV
      let csv = 'ID;Название;Артикул;Бренд;Склад;На складе;Резерв;Доступно;Цена\n';
      parts.forEach(part => {
        csv += `${part.id};${part.title};${part.original_number || part.manufacturer_number || ''};${part.brand_name};${part.warehouse_name};${part.stock};${part.reserve};${part.available};${part.price_opt}\n`;
      });
      
      const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `inventory_${new Date().toISOString().split('T')[0]}.csv`;
      link.click();
    } catch (error) {
      console.error('Ошибка экспорта:', error);
      alert('Ошибка экспорта остатков');
    }
  }
  
  onMount(() => {
    loadReferences();
    loadParts();
  });
</script>

<svelte:head>
  <title>Остатки склада - Admin</title>
</svelte:head>

<div class="space-y-6">
  <!-- Заголовок -->
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">Остатки склада</h1>
      <p class="text-gray-600 mt-2">Управление товарами и остатками</p>
    </div>
    <button
      onclick={handleAddProduct}
      class="btn-primary flex items-center"
    >
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
      Добавить товар
    </button>
  </div>
  
  <!-- Фильтры -->
  <div class="bg-white rounded-xl shadow-sm p-6">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
      <div class="lg:col-span-2">
        <label for="search" class="block text-sm font-medium text-gray-700 mb-2">
          Поиск товара
        </label>
        <input
          type="text"
          id="search"
          bind:value={filters.search}
          onchange={handleFilterChange}
          class="input w-full"
          placeholder="Название, артикул, бренд..."
        />
      </div>
      
      <div>
        <label for="brand" class="block text-sm font-medium text-gray-700 mb-2">
          Бренд
        </label>
        <select
          id="brand"
          bind:value={filters.brand}
          onchange={handleFilterChange}
          class="input w-full"
        >
          <option value="">Все бренды</option>
          {#each brands as brand}
            <option value={brand.id}>{brand.name}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="warehouse" class="block text-sm font-medium text-gray-700 mb-2">
          Склад
        </label>
        <select
          id="warehouse"
          bind:value={filters.warehouse}
          onchange={handleFilterChange}
          class="input w-full"
        >
          <option value="">Все склады</option>
          {#each warehouses as warehouse}
            <option value={warehouse.id}>{warehouse.name}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="stock_filter" class="block text-sm font-medium text-gray-700 mb-2">
          Остатки
        </label>
        <select
          id="stock_filter"
          bind:value={filters.stock_filter}
          onchange={handleFilterChange}
          class="input w-full"
        >
          {#each stockFilterOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
    </div>
    
    <!-- Кнопка экспорта -->
    <div class="mt-4 flex justify-end">
      <button
        onclick={exportToCSV}
        class="btn-outline flex items-center"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        Экспорт в CSV
      </button>
    </div>
  </div>
  
  <!-- Таблица товаров -->
  <div class="bg-white rounded-xl shadow-sm overflow-hidden">
    {#if isLoading}
      <div class="p-8 text-center">
        <div class="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-gray-600 mt-4">Загрузка товаров...</p>
      </div>
    {:else if parts.length > 0}
      <div class="overflow-x-auto">
        <table class="w-full table-auto">
          <thead class="bg-gray-50">
            <tr>
              <th class="text-left py-3 px-3 text-xs font-semibold text-gray-700">Товар</th>
              <th class="text-left py-3 px-3 text-xs font-semibold text-gray-700">Артикул</th>
              <th class="text-left py-3 px-3 text-xs font-semibold text-gray-700">Бренд</th>
              <th class="text-left py-3 px-3 text-xs font-semibold text-gray-700">Склад</th>
              <th class="text-center py-3 px-2 text-xs font-semibold text-gray-700">На скл.</th>
              <th class="text-center py-3 px-2 text-xs font-semibold text-gray-700">Резерв</th>
              <th class="text-center py-3 px-2 text-xs font-semibold text-gray-700">Доступ.</th>
              <th class="text-right py-3 px-3 text-xs font-semibold text-gray-700">Цена</th>
            </tr>
          </thead>
          <tbody>
            {#each parts as part}
              <tr class="border-t border-gray-100 hover:bg-gray-50 cursor-pointer" onclick={() => handlePartClick(part)}>
                <td class="py-3 px-3 max-w-[300px]">
                  <div class="flex items-center space-x-2">
                    {#if part.main_image?.url}
                      <img src={part.main_image.url} alt={part.title} class="w-10 h-10 object-cover rounded-lg flex-shrink-0" />
                    {:else}
                      <div class="w-10 h-10 bg-gray-200 rounded-lg flex-shrink-0"></div>
                    {/if}
                    <p class="text-xs font-medium text-primary-600 hover:text-primary-700 line-clamp-2 leading-tight">{part.title}</p>
                  </div>
                </td>
                <td class="py-3 px-3">
                  <span class="font-mono text-xs text-gray-600 break-all">
                    {part.original_number || part.manufacturer_number || '-'}
                  </span>
                </td>
                <td class="py-3 px-3 text-xs text-gray-600">{part.brand_name}</td>
                <td class="py-3 px-3 text-xs text-gray-600 max-w-[150px]">
                  <span class="line-clamp-2 leading-tight">{part.warehouse_name}</span>
                </td>
                <td class="py-3 px-2 text-xs text-center text-gray-900 font-medium">{part.stock}</td>
                <td class="py-3 px-2 text-xs text-center text-gray-600">{part.reserve}</td>
                <td class="py-3 px-2 text-center">
                  <span class="text-xs font-semibold {
                    part.available === 0 ? 'text-red-600' :
                    part.available <= 5 ? 'text-orange-600' :
                    'text-green-600'
                  }">
                    {part.available}
                  </span>
                </td>
                <td class="py-3 px-3 text-xs font-medium text-gray-900 text-right whitespace-nowrap">
                  {formatUtils.formatPrice(Number(part.price_opt))}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {:else}
      <div class="p-12 text-center">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Товары не найдены</h3>
        <p class="text-gray-600">Попробуйте изменить параметры поиска</p>
      </div>
    {/if}
  </div>
  
  <!-- Итого -->
  {#if !isLoading}
    <div class="bg-white rounded-xl shadow-sm p-6">
      <p class="text-sm text-gray-600">
        Отображено товаров: <span class="font-semibold text-gray-900">{parts.length}</span>
      </p>
    </div>
  {/if}
</div>

<!-- Модальное окно редактирования товара -->
<ProductEditModal 
  part={selectedPart}
  isOpen={isModalOpen}
  onClose={handleModalClose}
  onUpdate={handlePartUpdate}
/>

<!-- Модальное окно добавления товара -->
<AddProductModal 
  brands={brands}
  warehouses={warehouses}
  isOpen={isAddModalOpen}
  onClose={handleAddModalClose}
  onSuccess={handleProductAdded}
/>

