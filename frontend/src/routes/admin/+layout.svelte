<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { adminAuth } from '$lib/utils/admin-auth.js';
  import NotificationBell from '$lib/components/admin/NotificationBell.svelte';
  
  let { children } = $props();
  
  let isAuthenticated = $state(false);
  let currentPath = $derived($page.url.pathname);
  let currentUser = $state(null);
  
  // Проверка авторизации
  function checkAuth() {
    if (typeof window === 'undefined') return false;
    return adminAuth.isAuthenticated();
  }
  
  // Выход
  function handleLogout() {
    adminAuth.logout();
    goto('/admin');
  }
  
  // Проверка при монтировании
  onMount(() => {
    isAuthenticated = checkAuth();
    currentUser = adminAuth.getUser();
    
    // Если авторизован и на странице логина - редирект в дашборд
    if (isAuthenticated && currentPath === '/admin') {
      goto('/admin/dashboard');
    }
    // Если не авторизован и НЕ на странице логина - редирект на логин
    else if (!isAuthenticated && currentPath !== '/admin') {
      goto('/admin');
    }
  });
  
  // Активная ссылка
  function isActive(path) {
    return currentPath === path || currentPath.startsWith(path + '/');
  }
</script>

{#if isAuthenticated && currentPath !== '/admin'}
  <!-- Админ панель layout -->
  <div class="min-h-screen bg-gray-100">
    <!-- Шапка админки -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Логотип -->
          <div class="flex items-center space-x-4">
            <a href="/admin/dashboard" class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold">A</span>
              </div>
              <span class="text-xl font-bold text-gray-900">Admin Panel</span>
            </a>
          </div>
          
          <!-- Навигация -->
          <nav class="hidden md:flex items-center space-x-6">
            <a 
              href="/admin/dashboard" 
              class="px-3 py-2 rounded-lg transition-colors {isActive('/admin/dashboard') ? 'bg-primary-100 text-primary-700 font-semibold' : 'text-gray-700 hover:bg-gray-100'}"
            >
              Главная
            </a>
            <a 
              href="/admin/orders" 
              class="px-3 py-2 rounded-lg transition-colors {isActive('/admin/orders') ? 'bg-primary-100 text-primary-700 font-semibold' : 'text-gray-700 hover:bg-gray-100'}"
            >
              Заказы
            </a>
            <a 
              href="/admin/inventory" 
              class="px-3 py-2 rounded-lg transition-colors {isActive('/admin/inventory') ? 'bg-primary-100 text-primary-700 font-semibold' : 'text-gray-700 hover:bg-gray-100'}"
            >
              Остатки
            </a>
            <a 
              href="/admin/analytics" 
              class="px-3 py-2 rounded-lg transition-colors {isActive('/admin/analytics') ? 'bg-primary-100 text-primary-700 font-semibold' : 'text-gray-700 hover:bg-gray-100'}"
            >
              Аналитика
            </a>
            <a 
              href="/admin/finance" 
              class="px-3 py-2 rounded-lg transition-colors {isActive('/admin/finance') ? 'bg-primary-100 text-primary-700 font-semibold' : 'text-gray-700 hover:bg-gray-100'}"
            >
              Финансы
            </a>
            <a 
              href="/admin/customers" 
              class="px-3 py-2 rounded-lg transition-colors {isActive('/admin/customers') ? 'bg-primary-100 text-primary-700 font-semibold' : 'text-gray-700 hover:bg-gray-100'}"
            >
              Клиенты
            </a>
          </nav>
          
          <!-- Пользователь -->
          <div class="flex items-center space-x-4">
            <!-- Уведомления -->
            <NotificationBell />
            
            <a href="/" class="text-gray-600 hover:text-gray-900" target="_blank">
              На сайт
            </a>
            <button 
              onclick={handleLogout}
              class="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Контент -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {@render children()}
    </main>
  </div>
{:else}
  <!-- Страница логина или загрузка -->
  {@render children()}
{/if}

