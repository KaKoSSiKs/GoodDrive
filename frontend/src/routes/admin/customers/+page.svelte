<script>
  import { onMount } from 'svelte';
  import { crmApi, formatUtils } from '$lib/utils/api.js';
  
  let customers = $state([]);
  let isLoading = $state(true);
  let filters = $state({ search: '', category: '' });
  let deletingCustomer = $state(null);
  let showDeleteConfirm = $state(false);
  let isDeleting = $state(false);
  
  async function loadCustomers() {
    try {
      isLoading = true;
      const response = await crmApi.getCustomers({ ...filters, page_size: 100 });
      customers = response.results || response;
    } catch (error) {
      console.error('Error loading customers:', error);
    } finally {
      isLoading = false;
    }
  }
  
  async function syncCustomers() {
    if (!confirm('Синхронизировать клиентов из заказов?')) return;
    try {
      const result = await crmApi.syncFromOrders();
      alert(`Синхронизировано! Создано: ${result.created_count}, Всего: ${result.total_customers}`);
      loadCustomers();
    } catch (error) {
      alert('Ошибка синхронизации');
    }
  }
  
  function handleDeleteClick(customer) {
    deletingCustomer = customer;
    showDeleteConfirm = true;
  }
  
  async function handleDeleteCustomer(force = false) {
    if (!deletingCustomer) return;
    
    try {
      isDeleting = true;
      const result = await crmApi.deleteCustomer(deletingCustomer.id, force);
      
      alert(`Клиент ${deletingCustomer.name} успешно удален${result.warning ? '\n\n⚠️ ' + result.warning : ''}`);
      
      loadCustomers();
      showDeleteConfirm = false;
      deletingCustomer = null;
    } catch (error) {
      console.error('Ошибка удаления клиента:', error);
      
      // Проверяем, требуется ли force
      if (error.message?.includes('force')) {
        const shouldForce = confirm('У клиента есть заказы. Удалить клиента, но оставить заказы в системе?');
        if (shouldForce) {
          handleDeleteCustomer(true);
          return;
        }
      } else {
        alert('Ошибка удаления клиента');
      }
    } finally {
      isDeleting = false;
    }
  }
  
  onMount(() => {
    loadCustomers();
  });
</script>

<svelte:head>
  <title>Клиенты - Admin</title>
</svelte:head>

<div class="space-y-4 sm:space-y-6 w-full">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">Клиенты (CRM)</h1>
      <p class="text-gray-600 mt-2">Управление клиентской базой</p>
    </div>
    <button onclick={syncCustomers} class="btn-primary">Синхронизировать из заказов</button>
  </div>
  
  <div class="bg-white rounded-xl shadow-sm p-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
      <input type="text" bind:value={filters.search} onchange={loadCustomers} placeholder="Поиск..." class="input col-span-2" />
      <select bind:value={filters.category} onchange={loadCustomers} class="input">
        <option value="">Все категории</option>
        <option value="new">Новые</option>
        <option value="regular">Постоянные</option>
        <option value="vip">VIP</option>
        <option value="inactive">Неактивные</option>
      </select>
    </div>
    
    {#if isLoading}
      <div class="text-center py-8">Загрузка...</div>
    {:else if customers.length === 0}
      <div class="text-center py-12 text-gray-500">
        <p>Клиентов пока нет</p>
        <button onclick={syncCustomers} class="btn-outline mt-4">Синхронизировать из заказов</button>
      </div>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Клиент</th>
              <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Телефон</th>
              <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Категория</th>
              <th class="text-right py-3 px-4 text-sm font-semibold text-gray-700">Заказов</th>
              <th class="text-right py-3 px-4 text-sm font-semibold text-gray-700">Потрачено</th>
              <th class="text-right py-3 px-4 text-sm font-semibold text-gray-700">Средний чек</th>
              <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Последний заказ</th>
              <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700">Действия</th>
            </tr>
          </thead>
          <tbody>
            {#each customers as customer}
              <tr class="border-t border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 text-sm font-medium text-gray-900">{customer.name}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{customer.phone}</td>
                <td class="py-3 px-4">
                  <span class="px-2 py-1 text-xs font-medium rounded-full {
                    customer.category === 'vip' ? 'bg-purple-100 text-purple-700' :
                    customer.category === 'regular' ? 'bg-blue-100 text-blue-700' :
                    customer.category === 'new' ? 'bg-green-100 text-green-700' :
                    'bg-gray-100 text-gray-700'
                  }">
                    {customer.category_display}
                  </span>
                </td>
                <td class="py-3 px-4 text-sm text-gray-900 text-right">{customer.total_orders}</td>
                <td class="py-3 px-4 text-sm font-semibold text-gray-900 text-right">{formatUtils.formatPrice(Number(customer.total_spent))}</td>
                <td class="py-3 px-4 text-sm text-gray-600 text-right">{formatUtils.formatPrice(Number(customer.average_order))}</td>
                <td class="py-3 px-4 text-sm text-gray-600">
                  {customer.last_order_date ? new Date(customer.last_order_date).toLocaleDateString('ru-RU') : '-'}
                </td>
                <td class="py-3 px-4 text-center">
                  <button
                    onclick={() => handleDeleteClick(customer)}
                    class="text-red-600 hover:text-red-700 p-2 rounded-lg hover:bg-red-50 transition-colors"
                    title="Удалить клиента"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>

<!-- Модальное окно подтверждения удаления -->
{#if showDeleteConfirm && deletingCustomer}
  <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4" onclick={() => { showDeleteConfirm = false; deletingCustomer = null; }}>
    <div class="bg-white rounded-xl shadow-2xl max-w-md w-full" onclick={(e) => e.stopPropagation()}>
      <div class="p-6">
        <div class="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full">
          <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 text-center mb-2">Удалить клиента?</h3>
        <p class="text-sm text-gray-600 text-center mb-2">
          Вы уверены, что хотите удалить клиента <span class="font-semibold">{deletingCustomer.name}</span>?
        </p>
        <p class="text-xs text-gray-500 text-center mb-6">
          Телефон: {deletingCustomer.phone}<br />
          Заказов: {deletingCustomer.total_orders}<br />
          Это действие нельзя отменить.
        </p>
        <div class="flex space-x-3">
          <button
            onclick={() => { showDeleteConfirm = false; deletingCustomer = null; }}
            class="btn-outline flex-1"
            disabled={isDeleting}
          >
            Отмена
          </button>
          <button
            onclick={() => handleDeleteCustomer(false)}
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

