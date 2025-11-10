<script>
  import { ordersApi, formatUtils } from '$lib/utils/api.js';
  
  let { order, isOpen, onClose, onUpdate } = $props();
  
  let isUpdating = $state(false);
  let statusComment = $state('');
  let selectedStatus = $state(order?.status || 'new');
  let orderDetails = $state(null);
  let isLoadingDetails = $state(false);
  
  const statusOptions = [
    { value: 'new', label: 'Новый заказ', color: 'orange' },
    { value: 'processing', label: 'В обработке', color: 'indigo' },
    { value: 'shipped', label: 'Отправлен', color: 'purple' },
    { value: 'completed', label: 'Завершён', color: 'green' },
    { value: 'canceled', label: 'Отменён', color: 'red' }
  ];
  
  // Загрузка полной информации о заказе
  async function loadOrderDetails() {
    if (!order) return;
    
    try {
      isLoadingDetails = true;
      orderDetails = await ordersApi.getOrder(order.id);
      selectedStatus = orderDetails.status;
    } catch (error) {
      console.error('Ошибка загрузки деталей заказа:', error);
    } finally {
      isLoadingDetails = false;
    }
  }
  
  // Изменение статуса
  async function handleStatusChange() {
    if (!orderDetails || selectedStatus === orderDetails.status) return;
    
    try {
      isUpdating = true;
      await ordersApi.updateOrderStatus(orderDetails.id, selectedStatus, statusComment);
      
      // Перезагружаем детали
      await loadOrderDetails();
      statusComment = '';
      
      // Уведомляем родителя
      if (onUpdate) onUpdate();
      
      alert('Статус успешно изменён');
    } catch (error) {
      console.error('Ошибка обновления статуса:', error);
      alert('Ошибка изменения статуса');
    } finally {
      isUpdating = false;
    }
  }
  
  // Закрытие модалки
  function handleClose() {
    if (onClose) onClose();
  }
  
  // Загрузка при открытии
  $effect(() => {
    if (isOpen && order) {
      loadOrderDetails();
    }
  });
</script>

{#if isOpen}
  <!-- Overlay -->
  <div 
    class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
    onclick={handleClose}
  >
    <!-- Modal -->
    <div 
      class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto"
      onclick={(e) => e.stopPropagation()}
    >
      {#if isLoadingDetails}
        <!-- Загрузка -->
        <div class="p-12 text-center">
          <div class="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p class="text-gray-600">Загрузка деталей заказа...</p>
        </div>
      {:else if orderDetails}
        <!-- Заголовок -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Заказ #{orderDetails.order_number}</h2>
              <p class="text-sm text-gray-600 mt-1">
                Создан: {new Date(orderDetails.created_at).toLocaleString('ru-RU')}
              </p>
            </div>
            <button 
              onclick={handleClose}
              class="w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors"
            >
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- Кнопки печати -->
          <div class="flex space-x-2">
            <a 
              href={`http://localhost:8000/api/orders/${orderDetails.id}/print-invoice/`}
              target="_blank"
              class="btn-outline text-sm flex items-center"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Накладная
            </a>
            <a 
              href={`http://localhost:8000/api/orders/${orderDetails.id}/print-receipt/`}
              target="_blank"
              class="btn-outline text-sm flex items-center"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Чек
            </a>
          </div>
        </div>
        
        <!-- Контент -->
        <div class="p-6 space-y-6">
          <!-- Информация о клиенте -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-50 rounded-xl p-4">
              <h3 class="text-sm font-semibold text-gray-700 mb-3">Контактная информация</h3>
              <div class="space-y-2">
                <div>
                  <p class="text-xs text-gray-500">Имя клиента</p>
                  <p class="text-sm font-medium text-gray-900">{orderDetails.customer_name}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500">Телефон</p>
                  <a href="tel:{orderDetails.customer_phone}" class="text-sm font-medium text-primary-600 hover:text-primary-700">
                    {orderDetails.customer_phone}
                  </a>
                </div>
                {#if orderDetails.customer_email}
                  <div>
                    <p class="text-xs text-gray-500">Email</p>
                    <a href="mailto:{orderDetails.customer_email}" class="text-sm font-medium text-primary-600 hover:text-primary-700">
                      {orderDetails.customer_email}
                    </a>
                  </div>
                {/if}
              </div>
            </div>
            
            <div class="bg-gray-50 rounded-xl p-4">
              <h3 class="text-sm font-semibold text-gray-700 mb-3">Адрес доставки</h3>
              <div class="space-y-2">
                <div>
                  <p class="text-xs text-gray-500">Город</p>
                  <p class="text-sm font-medium text-gray-900">{orderDetails.delivery_city}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500">Адрес</p>
                  <p class="text-sm text-gray-900">{orderDetails.delivery_address}</p>
                </div>
                {#if orderDetails.delivery_postal_code}
                  <div>
                    <p class="text-xs text-gray-500">Индекс</p>
                    <p class="text-sm text-gray-900">{orderDetails.delivery_postal_code}</p>
                  </div>
                {/if}
              </div>
            </div>
          </div>
          
          <!-- Товары -->
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Состав заказа</h3>
            <div class="space-y-3">
              {#each orderDetails.items as item}
                <div class="flex items-center space-x-4 p-4 bg-gray-50 rounded-xl">
                  <!-- Изображение -->
                  {#if item.part.main_image?.url}
                    <img 
                      src={item.part.main_image.url} 
                      alt={item.part.title}
                      class="w-16 h-16 object-cover rounded-lg"
                    />
                  {:else}
                    <div class="w-16 h-16 bg-gray-200 rounded-lg"></div>
                  {/if}
                  
                  <!-- Информация -->
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-900 text-sm">{item.part.title}</h4>
                    <p class="text-xs text-gray-500">{item.part.brand_name}</p>
                    {#if item.part.original_number}
                      <p class="text-xs text-gray-500 font-mono">{item.part.original_number}</p>
                    {/if}
                  </div>
                  
                  <!-- Количество и цена -->
                  <div class="text-right">
                    <p class="text-sm text-gray-600">x{item.quantity} шт.</p>
                    <p class="text-sm font-semibold text-gray-900">{formatUtils.formatPrice(Number(item.unit_price))}</p>
                  </div>
                  
                  <div class="text-right">
                    <p class="text-xs text-gray-500">Итого</p>
                    <p class="text-lg font-bold text-primary-600">{formatUtils.formatPrice(Number(item.total_price))}</p>
                  </div>
                </div>
              {/each}
            </div>
          </div>
          
          <!-- Изменение статуса -->
          <div class="bg-blue-50 rounded-xl p-4">
            <h3 class="text-sm font-semibold text-gray-700 mb-3">Изменение статуса</h3>
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label for="status" class="block text-xs text-gray-600 mb-2">Текущий статус</label>
                  <select
                    id="status"
                    bind:value={selectedStatus}
                    class="input w-full"
                  >
                    {#each statusOptions as option}
                      <option value={option.value}>{option.label}</option>
                    {/each}
                  </select>
                </div>
                
                <div>
                  <label for="comment" class="block text-xs text-gray-600 mb-2">Комментарий</label>
                  <input
                    type="text"
                    id="comment"
                    bind:value={statusComment}
                    class="input w-full"
                    placeholder="Опционально..."
                  />
                </div>
              </div>
              
              {#if selectedStatus !== orderDetails.status}
                <button
                  onclick={handleStatusChange}
                  disabled={isUpdating}
                  class="btn-primary w-full disabled:opacity-50"
                >
                  {isUpdating ? 'Обновление...' : 'Изменить статус'}
                </button>
              {/if}
            </div>
          </div>
          
          <!-- История статусов -->
          {#if orderDetails.status_history && orderDetails.status_history.length > 0}
            <div>
              <h3 class="text-sm font-semibold text-gray-700 mb-3">История изменений</h3>
              <div class="space-y-2">
                {#each orderDetails.status_history as history}
                  <div class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg text-sm">
                    <div class="w-2 h-2 bg-primary-500 rounded-full mt-1.5"></div>
                    <div class="flex-1">
                      <p class="font-medium text-gray-900">
                        {statusOptions.find(s => s.value === history.status)?.label || history.status}
                      </p>
                      {#if history.comment}
                        <p class="text-gray-600 text-xs">{history.comment}</p>
                      {/if}
                      <p class="text-gray-500 text-xs mt-1">
                        {new Date(history.created_at).toLocaleString('ru-RU')}
                      </p>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
          
          <!-- Комментарии -->
          {#if orderDetails.notes}
            <div class="bg-yellow-50 rounded-xl p-4">
              <h3 class="text-sm font-semibold text-gray-700 mb-2">Комментарии клиента</h3>
              <p class="text-sm text-gray-700">{orderDetails.notes}</p>
            </div>
          {/if}
          
          <!-- Итого -->
          <div class="bg-gray-900 rounded-xl p-6 text-white">
            <div class="flex items-center justify-between">
              <span class="text-lg font-semibold">Общая сумма заказа</span>
              <span class="text-3xl font-bold">{formatUtils.formatPrice(Number(orderDetails.total_amount))}</span>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}

