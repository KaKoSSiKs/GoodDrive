// Утилиты для работы с API GoodDrive

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Базовый класс для работы с API
class ApiClient {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };
    
    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }
  
  async get(endpoint, params = {}) {
    const url = new URL(`${this.baseURL}${endpoint}`);
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
        url.searchParams.append(key, params[key]);
      }
    });

    // Use absolute URL to respect configured baseURL
    return this.request(url.toString());
  }
  
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  
  async patch(endpoint, data) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }
  
  async delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }
}

// Создаем экземпляр API клиента
const api = new ApiClient();

// API для работы с автозапчастями
export const partsApi = {
  // Получить список автозапчастей
  async getParts(params = {}) {
    return api.get('/api/parts/', params);
  },
  
  // Получить детали автозапчасти
  async getPart(id) {
    return api.get(`/api/parts/${id}/`);
  },
  
  // Получить похожие автозапчасти
  async getSimilarParts(id) {
    return api.get(`/api/parts/${id}/similar/`);
  },
  
  // Получить только доступные автозапчасти
  async getAvailableParts(params = {}) {
    return api.get('/api/parts/available/', params);
  },
  
  // Получить автозапчасти с низким остатком
  async getLowStockParts(params = {}) {
    return api.get('/api/parts/low_stock/', params);
  },
};

// API для работы с брендами
export const brandsApi = {
  // Получить список брендов
  async getBrands(params = {}) {
    return api.get('/api/brands/', params);
  },
  
  // Получить детали бренда
  async getBrand(id) {
    return api.get(`/api/brands/${id}/`);
  },
};

// API для работы со складами
export const warehousesApi = {
  // Получить список складов
  async getWarehouses(params = {}) {
    return api.get('/api/warehouses/', params);
  },
  
  // Получить детали склада
  async getWarehouse(id) {
    return api.get(`/api/warehouses/${id}/`);
  },
};

// API для работы с SEO
export const seoApi = {
  // Получить SEO метаданные для страницы
  async getPageMeta(slug) {
    return api.get(`/api/meta/${slug}/`);
  },
  
  // Получить глобальные SEO настройки
  async getSettings() {
    return api.get('/api/settings/');
  },
};

// API для работы с файлами
export const filesApi = {
  // Получить список файлов
  async getFiles(params = {}) {
    return api.get('/api/files/', params);
  },
  
  // Загрузить файл
  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return api.request('/api/files/', {
      method: 'POST',
      body: formData,
      headers: {}, // Убираем Content-Type для FormData
    });
  },
  
  // Удалить файл
  async deleteFile(id) {
    return api.delete(`/api/files/${id}/`);
  },
};

// API для работы с заказами
export const ordersApi = {
  // Создать заказ
  async createOrder(orderData) {
    return api.post('/api/orders/', orderData);
  },
  
  // Получить список заказов
  async getOrders(params = {}) {
    return api.get('/api/orders/', params);
  },
  
  // Получить заказ по ID
  async getOrder(id) {
    return api.get(`/api/orders/${id}/`);
  },
  
  // Обновить статус заказа
  async updateOrderStatus(id, status, comment = '') {
    return api.post(`/api/orders/${id}/update_status/`, {
      status,
      comment
    });
  },
  
  // Получить заказы по телефону
  async getOrdersByPhone(phone) {
    return api.get('/api/orders/by_phone/', { phone });
  },
  
  // Получить статистику заказов
  async getOrderStatistics() {
    return api.get('/api/orders/statistics/');
  },
  
  // Получить историю статусов заказа
  async getOrderStatusHistory(id) {
    return api.get(`/api/orders/${id}/status_history/`);
  },
};

// Утилиты для работы с корзиной
export const cartUtils = {
  // Получить корзину из localStorage
  getCart() {
    try {
      const cart = localStorage.getItem('gooddrive_cart');
      return cart ? JSON.parse(cart) : [];
    } catch (error) {
      console.error('Error loading cart:', error);
      return [];
    }
  },
  
  // Сохранить корзину в localStorage
  saveCart(cart) {
    try {
      localStorage.setItem('gooddrive_cart', JSON.stringify(cart));
    } catch (error) {
      console.error('Error saving cart:', error);
    }
  },
  
  // Добавить товар в корзину
  addToCart(part, quantity = 1) {
    const cart = this.getCart();
    const existingItem = cart.find(item => item.id === part.id);
    
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      const brandName = part.brand_name || part.brand?.name || '';
      const imageUrl = part.main_image?.url || part.images?.[0]?.image_url || null;
      const available = typeof part.available === 'number' ? part.available : (typeof part.quantity === 'number' ? part.quantity : 0);
      cart.push({
        id: part.id,
        title: part.title,
        brand: brandName,
        price: part.price_opt,
        image: imageUrl,
        quantity: quantity,
        available: available,
      });
    }
    
    this.saveCart(cart);
    this.notifyCartUpdate();
    return cart;
  },
  
  // Обновить количество товара в корзине
  updateQuantity(partId, quantity) {
    const cart = this.getCart();
    const item = cart.find(item => item.id === partId);
    
    if (item) {
      if (quantity <= 0) {
        this.removeFromCart(partId);
      } else {
        item.quantity = quantity;
        this.saveCart(cart);
        this.notifyCartUpdate();
      }
    }
    
    return this.getCart();
  },
  
  // Удалить товар из корзины
  removeFromCart(partId) {
    const cart = this.getCart();
    const updatedCart = cart.filter(item => item.id !== partId);
    this.saveCart(updatedCart);
    this.notifyCartUpdate();
    return updatedCart;
  },
  
  // Очистить корзину
  clearCart() {
    this.saveCart([]);
    this.notifyCartUpdate();
    return [];
  },
  
  // Уведомить об обновлении корзины
  notifyCartUpdate() {
    // Отправляем событие для обновления UI
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('cartUpdated'));
    }
  },
  
  // Получить общее количество товаров в корзине
  getTotalItems() {
    const cart = this.getCart();
    return cart.reduce((total, item) => total + item.quantity, 0);
  },
  
  // Получить общую стоимость корзины
  getTotalPrice() {
    const cart = this.getCart();
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  },
};

// Утилиты для форматирования
export const formatUtils = {
  // Форматирование цены
  formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(price);
  },
  
  // Форматирование числа
  formatNumber(number) {
    return new Intl.NumberFormat('ru-RU').format(number);
  },
  
  // Форматирование даты
  formatDate(date) {
    return new Intl.DateTimeFormat('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(new Date(date));
  },
  
  // Форматирование даты и времени
  formatDateTime(date) {
    return new Intl.DateTimeFormat('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(new Date(date));
  },
};

// Утилиты для валидации
export const validationUtils = {
  // Проверка email
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },
  
  // Проверка телефона
  isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
  },
  
  // Проверка цены
  isValidPrice(price) {
    return !isNaN(price) && price >= 0;
  },
  
  // Проверка количества
  isValidQuantity(quantity) {
    return Number.isInteger(quantity) && quantity > 0;
  },
};

// Экспортируем основной API клиент
export default api;
