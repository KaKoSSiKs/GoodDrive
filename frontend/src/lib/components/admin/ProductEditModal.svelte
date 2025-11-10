<script>
  import { formatUtils } from '$lib/utils/api.js';
  
  let { part, isOpen, onClose, onUpdate } = $props();
  
  let form = $state({
    title: '',
    price_opt: '',
    stock: '',
    reserve: '',
    description: ''
  });
  
  let isUpdating = $state(false);
  
  // Загрузка данных товара в форму
  $effect(() => {
    if (isOpen && part) {
      form.title = part.title;
      form.price_opt = part.price_opt;
      form.stock = part.stock;
      form.reserve = part.reserve;
      form.description = part.description || '';
    }
  });
  
  // Сохранение изменений
  async function handleSave() {
    try {
      isUpdating = true;
      
      // Тут будет API для обновления товара
      // Пока просто закрываем и уведомляем
      
      if (onUpdate) onUpdate();
      if (onClose) onClose();
      
      alert('Товар обновлён (функция в разработке)');
    } catch (error) {
      console.error('Ошибка обновления товара:', error);
      alert('Ошибка обновления товара');
    } finally {
      isUpdating = false;
    }
  }
  
  function handleClose() {
    if (onClose) onClose();
  }
</script>

{#if isOpen && part}
  <div 
    class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
    onclick={handleClose}
  >
    <div 
      class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
      onclick={(e) => e.stopPropagation()}
    >
      <!-- Заголовок -->
      <div class="p-6 border-b border-gray-200 flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Редактирование товара</h2>
          <p class="text-sm text-gray-500 mt-1">ID: {part.id}</p>
        </div>
        <button 
          onclick={handleClose}
          class="w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center"
        >
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- Форма -->
      <div class="p-6 space-y-6">
        <!-- Название -->
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
            Название товара
          </label>
          <input
            type="text"
            id="title"
            bind:value={form.title}
            class="input w-full"
            placeholder="Название товара"
          />
        </div>
        
        <!-- Цена -->
        <div>
          <label for="price" class="block text-sm font-medium text-gray-700 mb-2">
            Цена (₽)
          </label>
          <input
            type="number"
            id="price"
            bind:value={form.price_opt}
            step="0.01"
            class="input w-full"
            placeholder="0.00"
          />
        </div>
        
        <!-- Остатки -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="stock" class="block text-sm font-medium text-gray-700 mb-2">
              На складе
            </label>
            <input
              type="number"
              id="stock"
              bind:value={form.stock}
              class="input w-full"
              placeholder="0"
            />
          </div>
          
          <div>
            <label for="reserve" class="block text-sm font-medium text-gray-700 mb-2">
              В резерве
            </label>
            <input
              type="number"
              id="reserve"
              bind:value={form.reserve}
              class="input w-full"
              placeholder="0"
            />
          </div>
        </div>
        
        <!-- Описание -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
            Описание
          </label>
          <textarea
            id="description"
            bind:value={form.description}
            rows="4"
            class="input w-full"
            placeholder="Описание товара..."
          ></textarea>
        </div>
        
        <!-- Кнопки -->
        <div class="flex space-x-4">
          <button
            onclick={handleSave}
            disabled={isUpdating}
            class="btn-primary flex-1 disabled:opacity-50"
          >
            {isUpdating ? 'Сохранение...' : 'Сохранить'}
          </button>
          <button
            onclick={handleClose}
            class="btn-outline flex-1"
          >
            Отмена
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

