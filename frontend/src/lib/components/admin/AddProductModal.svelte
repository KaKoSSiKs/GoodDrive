<script>
  import { partsApi } from '$lib/utils/api.js';
  
  let { brands, warehouses, isOpen, onClose, onSuccess } = $props();
  
  let form = $state({
    title: '',
    brand: '',
    warehouse: '',
    price_opt: '',
    stock: 0,
    reserve: 0,
    original_number: '',
    manufacturer_number: '',
    description: '',
    image_url: ''
  });
  
  let isSubmitting = $state(false);
  let errors = $state({});
  
  function validateForm() {
    errors = {};
    let isValid = true;
    
    if (!form.title.trim()) {
      errors.title = 'Введите название';
      isValid = false;
    }
    
    if (!form.brand) {
      errors.brand = 'Выберите бренд';
      isValid = false;
    }
    
    if (!form.warehouse) {
      errors.warehouse = 'Выберите склад';
      isValid = false;
    }
    
    if (!form.price_opt || parseFloat(form.price_opt) <= 0) {
      errors.price_opt = 'Введите корректную цену';
      isValid = false;
    }
    
    return isValid;
  }
  
  async function handleSubmit(event) {
    event.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    try {
      isSubmitting = true;
      
      // Тут будет вызов API для создания товара
      // Пока заглушка
      
      alert('Товар создан (функция в разработке - требуется API endpoint)');
      
      if (onSuccess) onSuccess();
      if (onClose) onClose();
      
      // Сброс формы
      form = {
        title: '',
        brand: '',
        warehouse: '',
        price_opt: '',
        stock: 0,
        reserve: 0,
        original_number: '',
        manufacturer_number: '',
        description: '',
        image_url: ''
      };
    } catch (error) {
      console.error('Ошибка создания товара:', error);
      errors.general = 'Ошибка создания товара';
    } finally {
      isSubmitting = false;
    }
  }
  
  function handleClose() {
    if (onClose) onClose();
  }
</script>

{#if isOpen}
  <div 
    class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
    onclick={handleClose}
  >
    <div 
      class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
      onclick={(e) => e.stopPropagation()}
    >
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-2xl font-bold text-gray-900">Добавить товар</h2>
      </div>
      
      <form onsubmit={handleSubmit} class="p-6 space-y-6">
        <!-- Название -->
        <div>
          <label for="add-title" class="block text-sm font-medium text-gray-700 mb-2">
            Название <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="add-title"
            bind:value={form.title}
            class="input w-full {errors.title ? 'border-red-500' : ''}"
            placeholder="Название товара"
          />
          {#if errors.title}
            <p class="text-red-500 text-sm mt-1">{errors.title}</p>
          {/if}
        </div>
        
        <!-- Бренд и Склад -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="add-brand" class="block text-sm font-medium text-gray-700 mb-2">
              Бренд <span class="text-red-500">*</span>
            </label>
            <select
              id="add-brand"
              bind:value={form.brand}
              class="input w-full {errors.brand ? 'border-red-500' : ''}"
            >
              <option value="">Выберите бренд</option>
              {#each brands as brand}
                <option value={brand.id}>{brand.name}</option>
              {/each}
            </select>
            {#if errors.brand}
              <p class="text-red-500 text-sm mt-1">{errors.brand}</p>
            {/if}
          </div>
          
          <div>
            <label for="add-warehouse" class="block text-sm font-medium text-gray-700 mb-2">
              Склад <span class="text-red-500">*</span>
            </label>
            <select
              id="add-warehouse"
              bind:value={form.warehouse}
              class="input w-full {errors.warehouse ? 'border-red-500' : ''}"
            >
              <option value="">Выберите склад</option>
              {#each warehouses as warehouse}
                <option value={warehouse.id}>{warehouse.name}</option>
              {/each}
            </select>
            {#if errors.warehouse}
              <p class="text-red-500 text-sm mt-1">{errors.warehouse}</p>
            {/if}
          </div>
        </div>
        
        <!-- Артикулы -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="add-original" class="block text-sm font-medium text-gray-700 mb-2">
              Оригинальный номер
            </label>
            <input
              type="text"
              id="add-original"
              bind:value={form.original_number}
              class="input w-full"
              placeholder="123456"
            />
          </div>
          
          <div>
            <label for="add-manufacturer" class="block text-sm font-medium text-gray-700 mb-2">
              Номер производителя
            </label>
            <input
              type="text"
              id="add-manufacturer"
              bind:value={form.manufacturer_number}
              class="input w-full"
              placeholder="ABC123"
            />
          </div>
        </div>
        
        <!-- Цена и остатки -->
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label for="add-price" class="block text-sm font-medium text-gray-700 mb-2">
              Цена (₽) <span class="text-red-500">*</span>
            </label>
            <input
              type="number"
              id="add-price"
              bind:value={form.price_opt}
              step="0.01"
              class="input w-full {errors.price_opt ? 'border-red-500' : ''}"
              placeholder="0.00"
            />
            {#if errors.price_opt}
              <p class="text-red-500 text-sm mt-1">{errors.price_opt}</p>
            {/if}
          </div>
          
          <div>
            <label for="add-stock" class="block text-sm font-medium text-gray-700 mb-2">
              На складе
            </label>
            <input
              type="number"
              id="add-stock"
              bind:value={form.stock}
              class="input w-full"
              placeholder="0"
            />
          </div>
          
          <div>
            <label for="add-reserve" class="block text-sm font-medium text-gray-700 mb-2">
              Резерв
            </label>
            <input
              type="number"
              id="add-reserve"
              bind:value={form.reserve}
              class="input w-full"
              placeholder="0"
            />
          </div>
        </div>
        
        <!-- URL изображения -->
        <div>
          <label for="add-image" class="block text-sm font-medium text-gray-700 mb-2">
            URL изображения
          </label>
          <input
            type="url"
            id="add-image"
            bind:value={form.image_url}
            class="input w-full"
            placeholder="https://example.com/image.jpg"
          />
          <p class="text-xs text-gray-500 mt-1">Или используйте команду fetch_part_images после создания</p>
        </div>
        
        <!-- Описание -->
        <div>
          <label for="add-description" class="block text-sm font-medium text-gray-700 mb-2">
            Описание
          </label>
          <textarea
            id="add-description"
            bind:value={form.description}
            rows="4"
            class="input w-full"
            placeholder="Описание товара..."
          ></textarea>
        </div>
        
        {#if errors.general}
          <div class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-red-600 text-sm">{errors.general}</p>
          </div>
        {/if}
        
        <!-- Кнопки -->
        <div class="flex space-x-4">
          <button
            type="submit"
            disabled={isSubmitting}
            class="btn-primary flex-1 disabled:opacity-50"
          >
            {isSubmitting ? 'Создание...' : 'Создать товар'}
          </button>
          <button
            type="button"
            onclick={handleClose}
            class="btn-outline flex-1"
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}

