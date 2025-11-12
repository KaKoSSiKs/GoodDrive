<script>
  import { ordersApi, formatUtils } from '$lib/utils/api.js';
  
  let { order, isOpen, onClose, onUpdate } = $props();
  
  let isUpdating = $state(false);
  let statusComment = $state('');
  let selectedStatus = $state(order?.status || 'new');
  let orderDetails = $state(null);
  let isLoadingDetails = $state(false);
  let isDeleting = $state(false);
  let showDeleteConfirm = $state(false);
  
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
    showDeleteConfirm = false;
    if (onClose) onClose();
  }
  
  // Удаление заказа
  async function handleDeleteOrder() {
    if (!orderDetails) return;
    
    try {
      isDeleting = true;
      await ordersApi.deleteOrder(orderDetails.id);
      
      alert(`Заказ #${orderDetails.order_number} успешно удален`);
      
      // Уведомляем родителя и закрываем модалку
      if (onUpdate) onUpdate();
      if (onClose) onClose();
    } catch (error) {
      console.error('Ошибка удаления заказа:', error);
      alert('Ошибка удаления заказа');
    } finally {
      isDeleting = false;
      showDeleteConfirm = false;
    }
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
    class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-2 sm:p-4"
    onclick={handleClose}
  >
    <!-- Modal -->
    <div 
      class="bg-white rounded-xl sm:rounded-2xl shadow-2xl max-w-4xl w-full max-h-[95vh] overflow-y-auto"
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
        <div class="p-4 sm:p-6 border-b border-gray-200">
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
          
           <!-- Кнопки печати и удаления -->
           <div class="flex flex-wrap gap-2">
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
             <button
               onclick={() => showDeleteConfirm = true}
               class="btn-outline text-sm flex items-center text-red-600 border-red-300 hover:bg-red-50 ml-auto"
             >
               <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
               </svg>
               Удалить заказ
             </button>
           </div>
        </div>
        
        <!-- Контент -->
        <div class="p-4 sm:p-6 space-y-4 sm:space-y-6">
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
            <h3 class="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Состав заказа</h3>
            <div class="space-y-3">
              {#each orderDetails.items as item}
                <div class="bg-gray-50 rounded-xl p-3 sm:p-4">
                  <div class="flex items-start gap-3">
                    <!-- Изображение -->
                    {#if item.part.main_image?.url}
                      <img 
                        src={item.part.main_image.url} 
                        alt={item.part.title}
                        class="w-14 h-14 sm:w-16 sm:h-16 object-cover rounded-lg flex-shrink-0"
                      />
                    {:else}
                      <div class="w-14 h-14 sm:w-16 sm:h-16 bg-gray-200 rounded-lg flex-shrink-0"></div>
                    {/if}
                    
                    <!-- Информация -->
                    <div class="flex-1 min-w-0">
                      <h4 class="font-medium text-gray-900 text-sm sm:text-base mb-1 line-clamp-2">{item.part.title}</h4>
                      <p class="text-xs text-gray-500">{item.part.brand_name}</p>
                      {#if item.part.original_number}
                        <p class="text-xs text-gray-500 font-mono">{item.part.original_number}</p>
                      {/if}
                    </div>
                  </div>
                  
                  <!-- Количество и цена (отдельная строка) -->
                  <div class="mt-3 pt-3 border-t border-gray-200 grid grid-cols-3 gap-2 sm:gap-4">
                    <div>
                      <p class="text-xs text-gray-500">Количество</p>
                      <p class="text-sm font-medium text-gray-900 whitespace-nowrap">{item.quantity} шт.</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Цена за шт.</p>
                      <p class="text-sm font-medium text-gray-900 whitespace-nowrap">{formatUtils.formatPrice(Number(item.unit_price))}</p>
                    </div>
                    <div class="text-right">
                      <p class="text-xs text-gray-500">Итого</p>
                      <p class="text-base sm:text-lg font-bold text-primary-600 whitespace-nowrap">{formatUtils.formatPrice(Number(item.total_price))}</p>
                    </div>
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

<!-- Модальное окно подтверждения удаления -->
{#if showDeleteConfirm}
  <div class="fixed inset-0 bg-black bg-opacity-50 z-[60] flex items-center justify-center p-4" onclick={() => showDeleteConfirm = false}>
    <div class="bg-white rounded-xl shadow-2xl max-w-md w-full" onclick={(e) => e.stopPropagation()}>
      <div class="p-6">
        <div class="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full">
          <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 text-center mb-2">Удалить заказ?</h3>
        <p class="text-sm text-gray-600 text-center mb-6">
          Вы уверены, что хотите удалить заказ <span class="font-semibold">#{orderDetails?.order_number}</span>?<br />
          Это действие нельзя отменить.
        </p>
        <div class="flex space-x-3">
          <button
            onclick={() => showDeleteConfirm = false}
            class="btn-outline flex-1"
            disabled={isDeleting}
          >
            Отмена
          </button>
          <button
            onclick={handleDeleteOrder}
            class="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
            disabled={isDeleting}
          >
            {isDeleting ? 'Удаление...' : 'Удалить'}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

