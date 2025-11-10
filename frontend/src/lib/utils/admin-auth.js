// Утилиты для авторизации администраторов

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const adminAuth = {
  /**
   * Вход администратора
   */
  async login(username, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Ошибка авторизации');
      }

      const data = await response.json();
      
      // Сохраняем токен и данные пользователя
      localStorage.setItem('admin_token', data.token);
      localStorage.setItem('admin_user', JSON.stringify(data.user));
      
      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  /**
   * Проверка токена
   */
  async verify() {
    const token = localStorage.getItem('admin_token');
    
    if (!token) {
      return false;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/verify/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        // Токен невалиден - очищаем
        this.logout();
        return false;
      }

      return true;
    } catch (error) {
      console.error('Verify error:', error);
      this.logout();
      return false;
    }
  },

  /**
   * Выход
   */
  logout() {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
  },

  /**
   * Получить текущего пользователя
   */
  getUser() {
    const userStr = localStorage.getItem('admin_user');
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Получить токен
   */
  getToken() {
    return localStorage.getItem('admin_token');
  },

  /**
   * Проверка авторизации (синхронно)
   */
  isAuthenticated() {
    return !!this.getToken();
  }
};

