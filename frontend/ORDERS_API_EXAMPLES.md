# API Примеры для корзины и заказов

## 🛒 Корзина (Frontend)

### Добавление товара в корзину

```javascript
import { cartUtils } from '$lib/utils/api.js';

// Добавить товар в корзину
const part = {
  id: 1,
  title: "Тормозные колодки",
  brand_name: "Bosch",
  price_opt: 2500.00,
  main_image: {
    url: "/media/parts/1/brake_pads.jpg"
  },
  available: 15
};

const cart = cartUtils.addToCart(part, 2);
console.log('Товар добавлен в корзину:', cart);
```

### Управление корзиной

```javascript
// Получить корзину
const cart = cartUtils.getCart();

// Обновить количество товара
const updatedCart = cartUtils.updateQuantity(1, 3);

// Удалить товар
const updatedCart = cartUtils.removeFromCart(1);

// Очистить корзину
const emptyCart = cartUtils.clearCart();

// Получить общую стоимость
const totalPrice = cartUtils.getTotalPrice();

// Получить количество товаров
const totalItems = cartUtils.getTotalItems();
```

### Структура товара в корзине

```javascript
const cartItem = {
  id: 1,                    // ID товара
  title: "Тормозные колодки", // Название
  brand: "Bosch",           // Бренд
  price: 2500.00,          // Цена за единицу
  image: "/media/parts/1/brake_pads.jpg", // Изображение
  quantity: 2,             // Количество
  available: 15            // Доступно на складе
};
```

## 📦 Заказы (Backend API)

### Создание заказа

```javascript
import { ordersApi } from '$lib/utils/api.js';

const orderData = {
  customer_name: "Иван Иванов",
  customer_phone: "+7 (999) 123-45-67",
  customer_email: "ivan@example.com",
  delivery_address: "ул. Ленина, д. 10, кв. 5",
  delivery_city: "Москва",
  delivery_postal_code: "123456",
  notes: "Позвонить перед доставкой",
  items: [
    {
      part_id: 1,
      quantity: 2
    },
    {
      part_id: 2,
      quantity: 1
    }
  ]
};

const order = await ordersApi.createOrder(orderData);
console.log('Заказ создан:', order);
```

### Пример ответа создания заказа

```json
{
  "id": 1,
  "order_number": "GD20240115103000ABC12345",
  "customer_name": "Иван Иванов",
  "customer_phone": "+7 (999) 123-45-67",
  "customer_email": "ivan@example.com",
  "delivery_address": "ул. Ленина, д. 10, кв. 5",
  "delivery_city": "Москва",
  "delivery_postal_code": "123456",
  "total_amount": "7500.00",
  "status": "pending",
  "status_display": "Ожидает обработки",
  "notes": "Позвонить перед доставкой",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "items": [
    {
      "id": 1,
      "part": {
        "id": 1,
        "title": "Тормозные колодки",
        "brand_name": "Bosch",
        "price_opt": 2500.00,
        "main_image": {
          "url": "/media/parts/1/brake_pads.jpg"
        }
      },
      "quantity": 2,
      "unit_price": "2500.00",
      "total_price": "5000.00"
    },
    {
      "id": 2,
      "part": {
        "id": 2,
        "title": "Масляный фильтр",
        "brand_name": "Mann",
        "price_opt": 2500.00,
        "main_image": {
          "url": "/media/parts/2/oil_filter.jpg"
        }
      },
      "quantity": 1,
      "unit_price": "2500.00",
      "total_price": "2500.00"
    }
  ],
  "status_history": [
    {
      "id": 1,
      "status": "pending",
      "comment": "Заказ создан",
      "created_at": "2024-01-15T10:30:00Z",
      "created_by_name": null
    }
  ]
}
```

### Получение заказов

```javascript
// Получить все заказы
const orders = await ordersApi.getOrders();

// Получить заказы с фильтрами
const filteredOrders = await ordersApi.getOrders({
  status: 'pending',
  customer_phone: '+7 (999) 123-45-67',
  ordering: '-created_at'
});

// Получить заказ по ID
const order = await ordersApi.getOrder(1);

// Получить заказы по телефону
const ordersByPhone = await ordersApi.getOrdersByPhone('+7 (999) 123-45-67');
```

### Обновление статуса заказа

```javascript
// Обновить статус заказа
const updatedOrder = await ordersApi.updateOrderStatus(1, 'processing', 'Заказ взят в работу');

// Получить историю статусов
const statusHistory = await ordersApi.getOrderStatusHistory(1);
```

### Статистика заказов

```javascript
// Получить статистику
const statistics = await ordersApi.getOrderStatistics();

// Пример ответа
{
  "total_orders": 150,
  "total_amount": 1250000.00,
  "avg_order_amount": 8333.33,
  "status_statistics": [
    {"status": "pending", "count": 25},
    {"status": "processing", "count": 15},
    {"status": "shipped", "count": 80},
    {"status": "delivered", "count": 25},
    {"status": "cancelled", "count": 5}
  ],
  "recent_30_days": {
    "orders_count": 45,
    "total_amount": 375000.00
  }
}
```

## 🔧 Компоненты Frontend

### Страница корзины (/cart)

```svelte
<script>
  import { onMount } from 'svelte';
  import { cartUtils, formatUtils } from '$lib/utils/api.js';
  
  let cart = $state([]);
  let isLoading = $state(false);
  
  const totalItems = $derived(cart.reduce((total, item) => total + item.quantity, 0));
  const totalPrice = $derived(cart.reduce((total, item) => total + (item.price * item.quantity), 0));
  const isEmpty = $derived(cart.length === 0);
  
  function loadCart() {
    cart = cartUtils.getCart();
  }
  
  function updateQuantity(itemId, newQuantity) {
    if (newQuantity <= 0) {
      removeItem(itemId);
    } else {
      cart = cartUtils.updateQuantity(itemId, newQuantity);
    }
  }
  
  function removeItem(itemId) {
    cart = cartUtils.removeFromCart(itemId);
  }
  
  function clearCart() {
    if (confirm('Вы уверены, что хотите очистить корзину?')) {
      cart = cartUtils.clearCart();
    }
  }
  
  function proceedToCheckout() {
    if (isEmpty) return;
    window.location.href = '/checkout';
  }
  
  onMount(() => {
    loadCart();
  });
</script>

<div class="container-custom py-8">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-neutral-900 mb-8">Корзина</h1>
    
    {#if isEmpty}
      <!-- Пустая корзина -->
      <div class="text-center py-16">
        <h2 class="text-2xl font-bold text-neutral-900 mb-4">Корзина пуста</h2>
        <a href="/catalog" class="btn-primary">Перейти в каталог</a>
      </div>
    {:else}
      <!-- Содержимое корзины -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Список товаров -->
        <div class="lg:col-span-2">
          <div class="card p-6">
            <div class="space-y-4">
              {#each cart as item}
                <div class="flex items-center space-x-4 p-4 border border-neutral-200 rounded-lg">
                  <!-- Изображение -->
                  <div class="w-20 h-20 bg-neutral-100 rounded-lg flex items-center justify-center">
                    {#if item.image}
                      <img src={item.image} alt={item.title} class="w-full h-full object-cover rounded-lg" />
                    {:else}
                      <svg class="w-8 h-8 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    {/if}
                  </div>
                  
                  <!-- Информация -->
                  <div class="flex-1 min-w-0">
                    <h3 class="font-semibold text-neutral-900 truncate">{item.title}</h3>
                    <p class="text-sm text-neutral-600">{item.brand}</p>
                    <p class="text-lg font-bold text-primary-500">{formatUtils.formatPrice(item.price)}</p>
                  </div>
                  
                  <!-- Управление количеством -->
                  <div class="flex items-center space-x-2">
                    <button on:click={() => updateQuantity(item.id, item.quantity - 1)} class="w-8 h-8 rounded-full border border-neutral-300 flex items-center justify-center hover:bg-neutral-50">-</button>
                    <span class="w-12 text-center font-medium">{item.quantity}</span>
                    <button on:click={() => updateQuantity(item.id, item.quantity + 1)} class="w-8 h-8 rounded-full border border-neutral-300 flex items-center justify-center hover:bg-neutral-50">+</button>
                  </div>
                  
                  <!-- Общая цена -->
                  <div class="text-right">
                    <p class="text-lg font-bold text-neutral-900">{formatUtils.formatPrice(item.price * item.quantity)}</p>
                  </div>
                  
                  <!-- Удаление -->
                  <button on:click={() => removeItem(item.id)} class="text-neutral-400 hover:text-red-600 p-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              {/each}
            </div>
          </div>
        </div>
        
        <!-- Итоговая информация -->
        <div class="lg:col-span-1">
          <div class="card p-6 sticky top-24">
            <h2 class="text-xl font-semibold text-neutral-900 mb-6">Итого</h2>
            
            <div class="space-y-4 mb-6">
              <div class="flex justify-between">
                <span class="text-neutral-600">Товары ({totalItems} шт.)</span>
                <span class="font-medium">{formatUtils.formatPrice(totalPrice)}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-neutral-600">Доставка</span>
                <span class="font-medium text-green-600">Бесплатно</span>
              </div>
              
              <div class="border-t border-neutral-200 pt-4">
                <div class="flex justify-between">
                  <span class="text-lg font-semibold text-neutral-900">Общая сумма</span>
                  <span class="text-lg font-bold text-primary-500">{formatUtils.formatPrice(totalPrice)}</span>
                </div>
              </div>
            </div>
            
            <button on:click={proceedToCheckout} class="btn-primary w-full mb-4">Оформить заказ</button>
            <a href="/catalog" class="btn-outline w-full text-center">Продолжить покупки</a>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
```

### Форма оформления заказа (/checkout)

```svelte
<script>
  import { onMount } from 'svelte';
  import { cartUtils, ordersApi, formatUtils, validationUtils } from '$lib/utils/api.js';
  
  let cart = $state([]);
  let isSubmitting = $state(false);
  let orderSuccess = $state(false);
  let orderData = $state(null);
  
  let form = $state({
    customer_name: '',
    customer_phone: '',
    customer_email: '',
    delivery_address: '',
    delivery_city: '',
    delivery_postal_code: '',
    notes: ''
  });
  
  let errors = $state({});
  
  const totalItems = $derived(cart.reduce((total, item) => total + item.quantity, 0));
  const totalPrice = $derived(cart.reduce((total, item) => total + (item.price * item.quantity), 0));
  const isEmpty = $derived(cart.length === 0);
  
  function loadCart() {
    cart = cartUtils.getCart();
  }
  
  function validateForm() {
    errors = {};
    let isValid = true;
    
    if (!form.customer_name.trim()) {
      errors.customer_name = 'Введите имя';
      isValid = false;
    }
    
    if (!form.customer_phone.trim()) {
      errors.customer_phone = 'Введите номер телефона';
      isValid = false;
    } else if (!validationUtils.isValidPhone(form.customer_phone)) {
      errors.customer_phone = 'Введите корректный номер телефона';
      isValid = false;
    }
    
    if (form.customer_email && !validationUtils.isValidEmail(form.customer_email)) {
      errors.customer_email = 'Введите корректный email';
      isValid = false;
    }
    
    if (!form.delivery_address.trim()) {
      errors.delivery_address = 'Введите адрес доставки';
      isValid = false;
    }
    
    if (!form.delivery_city.trim()) {
      errors.delivery_city = 'Введите город';
      isValid = false;
    }
    
    return isValid;
  }
  
  async function handleSubmit(event) {
    event.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    isSubmitting = true;
    
    try {
      const orderData = {
        customer_name: form.customer_name.trim(),
        customer_phone: form.customer_phone.trim(),
        customer_email: form.customer_email.trim() || null,
        delivery_address: form.delivery_address.trim(),
        delivery_city: form.delivery_city.trim(),
        delivery_postal_code: form.delivery_postal_code.trim() || null,
        notes: form.notes.trim() || null,
        items: cart.map(item => ({
          part_id: item.id,
          quantity: item.quantity
        }))
      };
      
      const response = await ordersApi.createOrder(orderData);
      orderData = response;
      
      cartUtils.clearCart();
      cart = [];
      orderSuccess = true;
      
    } catch (error) {
      console.error('Ошибка создания заказа:', error);
      errors.general = 'Ошибка создания заказа. Попробуйте позже';
    } finally {
      isSubmitting = false;
    }
  }
  
  onMount(() => {
    loadCart();
    if (isEmpty) {
      window.location.href = '/cart';
    }
  });
</script>

{#if orderSuccess}
  <!-- Страница успешного заказа -->
  <div class="container-custom py-8">
    <div class="max-w-2xl mx-auto text-center">
      <div class="card p-8">
        <h1 class="text-3xl font-bold text-neutral-900 mb-4">Заказ успешно оформлен!</h1>
        <p class="text-neutral-600 mb-6">Ваш заказ #{orderData.order_number} принят в обработку.</p>
        
        <div class="bg-neutral-50 rounded-lg p-6 mb-8">
          <h2 class="text-lg font-semibold text-neutral-900 mb-4">Детали заказа</h2>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-neutral-600">Номер заказа:</span>
              <span class="font-medium">{orderData.order_number}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-600">Сумма:</span>
              <span class="font-medium">{formatUtils.formatPrice(orderData.total_amount)}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-600">Статус:</span>
              <span class="font-medium text-green-600">{orderData.status_display}</span>
            </div>
          </div>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4">
          <a href="/catalog" class="btn-primary">Продолжить покупки</a>
          <a href="/" class="btn-outline">На главную</a>
        </div>
      </div>
    </div>
  </div>
{:else}
  <!-- Форма оформления заказа -->
  <div class="container-custom py-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold text-neutral-900 mb-8">Оформление заказа</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Форма -->
        <div class="lg:col-span-2">
          <form on:submit={handleSubmit} class="space-y-8">
            <!-- Контактная информация -->
            <div class="card p-6">
              <h2 class="text-xl font-semibold text-neutral-900 mb-6">Контактная информация</h2>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="customer_name" class="block text-sm font-medium text-neutral-700 mb-2">
                    Имя <span class="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="customer_name"
                    bind:value={form.customer_name}
                    class="input {errors.customer_name ? 'border-red-500' : ''}"
                    placeholder="Введите ваше имя"
                  />
                  {#if errors.customer_name}
                    <p class="text-red-500 text-sm mt-1">{errors.customer_name}</p>
                  {/if}
                </div>
                
                <div>
                  <label for="customer_phone" class="block text-sm font-medium text-neutral-700 mb-2">
                    Телефон <span class="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    id="customer_phone"
                    bind:value={form.customer_phone}
                    class="input {errors.customer_phone ? 'border-red-500' : ''}"
                    placeholder="+7 (XXX) XXX-XX-XX"
                  />
                  {#if errors.customer_phone}
                    <p class="text-red-500 text-sm mt-1">{errors.customer_phone}</p>
                  {/if}
                </div>
                
                <div class="md:col-span-2">
                  <label for="customer_email" class="block text-sm font-medium text-neutral-700 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    id="customer_email"
                    bind:value={form.customer_email}
                    class="input {errors.customer_email ? 'border-red-500' : ''}"
                    placeholder="your@email.com"
                  />
                  {#if errors.customer_email}
                    <p class="text-red-500 text-sm mt-1">{errors.customer_email}</p>
                  {/if}
                </div>
              </div>
            </div>
            
            <!-- Адрес доставки -->
            <div class="card p-6">
              <h2 class="text-xl font-semibold text-neutral-900 mb-6">Адрес доставки</h2>
              
              <div class="space-y-6">
                <div>
                  <label for="delivery_city" class="block text-sm font-medium text-neutral-700 mb-2">
                    Город <span class="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="delivery_city"
                    bind:value={form.delivery_city}
                    class="input {errors.delivery_city ? 'border-red-500' : ''}"
                    placeholder="Введите город"
                  />
                  {#if errors.delivery_city}
                    <p class="text-red-500 text-sm mt-1">{errors.delivery_city}</p>
                  {/if}
                </div>
                
                <div>
                  <label for="delivery_address" class="block text-sm font-medium text-neutral-700 mb-2">
                    Адрес <span class="text-red-500">*</span>
                  </label>
                  <textarea
                    id="delivery_address"
                    bind:value={form.delivery_address}
                    class="input {errors.delivery_address ? 'border-red-500' : ''}"
                    rows="3"
                    placeholder="Введите полный адрес доставки"
                  ></textarea>
                  {#if errors.delivery_address}
                    <p class="text-red-500 text-sm mt-1">{errors.delivery_address}</p>
                  {/if}
                </div>
                
                <div>
                  <label for="delivery_postal_code" class="block text-sm font-medium text-neutral-700 mb-2">
                    Почтовый индекс
                  </label>
                  <input
                    type="text"
                    id="delivery_postal_code"
                    bind:value={form.delivery_postal_code}
                    class="input"
                    placeholder="123456"
                  />
                </div>
              </div>
            </div>
            
            <!-- Комментарии -->
            <div class="card p-6">
              <h2 class="text-xl font-semibold text-neutral-900 mb-6">Дополнительно</h2>
              
              <div>
                <label for="notes" class="block text-sm font-medium text-neutral-700 mb-2">
                  Комментарии к заказу
                </label>
                <textarea
                  id="notes"
                  bind:value={form.notes}
                  class="input"
                  rows="4"
                  placeholder="Дополнительная информация о заказе..."
                ></textarea>
              </div>
            </div>
            
            <!-- Общая ошибка -->
            {#if errors.general}
              <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-red-600">{errors.general}</p>
              </div>
            {/if}
            
            <!-- Кнопки -->
            <div class="flex flex-col sm:flex-row gap-4">
              <button
                type="submit"
                disabled={isSubmitting}
                class="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Оформление заказа...' : 'Оформить заказ'}
              </button>
              <a href="/cart" class="btn-outline">Вернуться в корзину</a>
            </div>
          </form>
        </div>
        
        <!-- Итоговая информация -->
        <div class="lg:col-span-1">
          <div class="card p-6 sticky top-24">
            <h2 class="text-xl font-semibold text-neutral-900 mb-6">Ваш заказ</h2>
            
            <!-- Список товаров -->
            <div class="space-y-4 mb-6">
              {#each cart as item}
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-12 bg-neutral-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    {#if item.image}
                      <img src={item.image} alt={item.title} class="w-full h-full object-cover rounded-lg" />
                    {:else}
                      <svg class="w-6 h-6 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    {/if}
                  </div>
                  
                  <div class="flex-1 min-w-0">
                    <h3 class="font-medium text-neutral-900 text-sm truncate">{item.title}</h3>
                    <p class="text-xs text-neutral-600">{item.brand}</p>
                    <p class="text-sm text-neutral-600">x{item.quantity}</p>
                  </div>
                  
                  <div class="text-sm font-medium text-neutral-900">
                    {formatUtils.formatPrice(item.price * item.quantity)}
                  </div>
                </div>
              {/each}
            </div>
            
            <!-- Итого -->
            <div class="border-t border-neutral-200 pt-4">
              <div class="flex justify-between mb-2">
                <span class="text-neutral-600">Товары ({totalItems} шт.)</span>
                <span class="font-medium">{formatUtils.formatPrice(totalPrice)}</span>
              </div>
              
              <div class="flex justify-between mb-2">
                <span class="text-neutral-600">Доставка</span>
                <span class="font-medium text-green-600">Бесплатно</span>
              </div>
              
              <div class="border-t border-neutral-200 pt-2">
                <div class="flex justify-between">
                  <span class="text-lg font-semibold text-neutral-900">Общая сумма</span>
                  <span class="text-lg font-bold text-primary-500">{formatUtils.formatPrice(totalPrice)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}
```

## 🔧 Валидация и обработка ошибок

### Валидация формы

```javascript
function validateForm() {
  errors = {};
  let isValid = true;
  
  // Имя
  if (!form.customer_name.trim()) {
    errors.customer_name = 'Введите имя';
    isValid = false;
  }
  
  // Телефон
  if (!form.customer_phone.trim()) {
    errors.customer_phone = 'Введите номер телефона';
    isValid = false;
  } else if (!validationUtils.isValidPhone(form.customer_phone)) {
    errors.customer_phone = 'Введите корректный номер телефона';
    isValid = false;
  }
  
  // Email (необязательный)
  if (form.customer_email && !validationUtils.isValidEmail(form.customer_email)) {
    errors.customer_email = 'Введите корректный email';
    isValid = false;
  }
  
  // Адрес доставки
  if (!form.delivery_address.trim()) {
    errors.delivery_address = 'Введите адрес доставки';
    isValid = false;
  }
  
  // Город
  if (!form.delivery_city.trim()) {
    errors.delivery_city = 'Введите город';
    isValid = false;
  }
  
  return isValid;
}
```

### Обработка ошибок API

```javascript
try {
  const order = await ordersApi.createOrder(orderData);
  // Успешное создание заказа
} catch (error) {
  console.error('Ошибка создания заказа:', error);
  
  if (error.message.includes('400')) {
    errors.general = 'Проверьте правильность заполнения формы';
  } else if (error.message.includes('500')) {
    errors.general = 'Произошла ошибка сервера. Попробуйте позже';
  } else {
    errors.general = 'Ошибка создания заказа. Попробуйте позже';
  }
}
```

## 📱 Мобильная оптимизация

### Адаптивная сетка

```css
/* Мобильные устройства */
@media (max-width: 768px) {
  .cart-grid {
    @apply grid-cols-1 gap-4;
  }
  
  .checkout-grid {
    @apply grid-cols-1 gap-6;
  }
}

/* Планшеты */
@media (min-width: 768px) and (max-width: 1024px) {
  .cart-grid {
    @apply grid-cols-1 gap-6;
  }
}

/* Десктоп */
@media (min-width: 1024px) {
  .cart-grid {
    @apply grid-cols-3 gap-8;
  }
  
  .checkout-grid {
    @apply grid-cols-3 gap-8;
  }
}
```

### Touch события

```svelte
<!-- Swipe для удаления товара -->
<div 
  class="cart-item"
  on:touchstart={handleTouchStart}
  on:touchmove={handleTouchMove}
  on:touchend={handleTouchEnd}
>
  <!-- Содержимое товара -->
</div>
```

## 🚀 Производительность

### Оптимизации

1. **Ленивая загрузка изображений:**
```svelte
<img 
  src={item.image} 
  alt={item.title}
  loading="lazy"
  class="w-full h-full object-cover rounded-lg"
/>
```

2. **Debounce для валидации:**
```javascript
import { debounce } from 'lodash-es';

const debouncedValidate = debounce(() => {
  validateForm();
}, 300);
```

3. **Кэширование корзины:**
```javascript
// Простое кэширование в памяти
const cartCache = new Map();

function getCachedCart(key) {
  if (cartCache.has(key)) {
    return cartCache.get(key);
  }
  
  const cart = cartUtils.getCart();
  cartCache.set(key, cart);
  return cart;
}
```

## 🧪 Тестирование

### Unit тесты

```javascript
// Тест корзины
import { cartUtils } from '$lib/utils/api.js';

test('adds item to cart', () => {
  const part = {
    id: 1,
    title: 'Test Part',
    brand_name: 'Test Brand',
    price_opt: 1000,
    available: 5
  };
  
  const cart = cartUtils.addToCart(part, 2);
  
  expect(cart).toHaveLength(1);
  expect(cart[0].quantity).toBe(2);
  expect(cart[0].title).toBe('Test Part');
});
```

### E2E тесты

```javascript
// Тест оформления заказа
test('creates order successfully', async ({ page }) => {
  await page.goto('/cart');
  
  // Добавляем товар в корзину
  await page.click('[data-testid="add-to-cart"]');
  
  // Переходим к оформлению
  await page.click('[data-testid="proceed-to-checkout"]');
  
  // Заполняем форму
  await page.fill('[name="customer_name"]', 'Иван Иванов');
  await page.fill('[name="customer_phone"]', '+7 (999) 123-45-67');
  await page.fill('[name="delivery_address"]', 'ул. Ленина, д. 10');
  await page.fill('[name="delivery_city"]', 'Москва');
  
  // Отправляем заказ
  await page.click('[type="submit"]');
  
  // Проверяем успех
  await expect(page.locator('[data-testid="order-success"]')).toBeVisible();
});
```

