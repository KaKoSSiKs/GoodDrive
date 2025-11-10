# Исправление отображения изображений в корзине

## Проблема

Изображения товаров не отображались в корзине и на странице оформления заказа, вместо них показывались серые плейсхолдеры с иконкой "изображение не найдено".

## Причина

API бэкенда возвращал относительные URL изображений (например, `/media/parts/...`), которые сохранялись в localStorage корзины. При попытке отобразить эти изображения, браузер не мог определить, к какому серверу обращаться, так как отсутствовал базовый URL.

## Решение

### 1. Добавлена утилита для преобразования URL изображений

В файле `frontend/src/lib/utils/api.js` добавлена новая утилита `imageUtils`:

```javascript
export const imageUtils = {
  getAbsoluteUrl(imageUrl) {
    if (!imageUrl) return null;
    // Если URL уже абсолютный, возвращаем как есть
    if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
      return imageUrl;
    }
    // Если URL относительный, добавляем базовый URL
    return `${API_BASE_URL}${imageUrl.startsWith('/') ? imageUrl : '/' + imageUrl}`;
  }
};
```

### 2. Обновлена функция добавления товаров в корзину

В `cartUtils.addToCart()` добавлено преобразование относительных URL в абсолютные при сохранении товара в корзину:

```javascript
let imageUrl = part.main_image?.url || part.images?.[0]?.image_url || null;
imageUrl = this.getAbsoluteImageUrl(imageUrl);
```

### 3. Добавлена миграция существующих данных корзины

В `cartUtils.getCart()` добавлена автоматическая миграция товаров с относительными URL:

```javascript
const migratedCart = parsedCart.map(item => {
  if (item.image && !item.image.startsWith('http://') && !item.image.startsWith('https://')) {
    return {
      ...item,
      image: this.getAbsoluteImageUrl(item.image)
    };
  }
  return item;
});
```

### 4. Обновлены компоненты для использования утилиты

Следующие компоненты были обновлены для использования `imageUtils.getAbsoluteUrl()`:

- `frontend/src/lib/components/PartCard.svelte` - карточка товара в каталоге
- `frontend/src/routes/product/[id]/+page.svelte` - страница товара
- `frontend/src/lib/components/SearchAutocomplete.svelte` - автокомплит поиска

### 5. Исправлена конфигурация Docker Compose

В `docker-compose.yml` исправлена переменная окружения:

```yaml
environment:
  - VITE_API_URL=http://localhost:8000
```

## Настройка переменных окружения

### Для локальной разработки

Создайте файл `frontend/.env` со следующим содержимым:

```env
VITE_API_URL=http://localhost:8000
```

### Для production

В production окружении настройте переменную `VITE_API_URL` на фактический URL вашего API сервера:

```env
VITE_API_URL=https://your-domain.com
```

## Проверка работы

1. Очистите кэш браузера и localStorage
2. Запустите проект:
   ```bash
   docker-compose up --build
   ```
3. Добавьте товары в корзину
4. Проверьте, что изображения отображаются корректно в:
   - Каталоге товаров
   - Корзине
   - Странице оформления заказа
   - Странице товара
   - Автокомплите поиска

## Изменённые файлы

1. `frontend/src/lib/utils/api.js` - добавлена утилита `imageUtils`
2. `frontend/src/lib/components/PartCard.svelte` - использует `imageUtils`
3. `frontend/src/routes/product/[id]/+page.svelte` - использует `imageUtils`
4. `frontend/src/lib/components/SearchAutocomplete.svelte` - использует `imageUtils`
5. `frontend/src/routes/cart/+page.svelte` - изображения теперь отображаются корректно
6. `frontend/src/routes/checkout/+page.svelte` - изображения теперь отображаются корректно
7. `docker-compose.yml` - исправлена переменная `VITE_API_URL`

## Дополнительные рекомендации

1. **Проверьте настройки CORS** на бэкенде, чтобы разрешить запросы изображений с фронтенда
2. **Убедитесь, что медиа-файлы доступны** через веб-сервер (например, nginx)
3. **Для production** рекомендуется использовать CDN для хранения изображений
4. **Оптимизируйте изображения** перед загрузкой (размер, формат)

## Поддержка

Если изображения по-прежнему не отображаются:

1. Проверьте консоль браузера на наличие ошибок 404 или CORS
2. Убедитесь, что переменная `VITE_API_URL` установлена корректно
3. Проверьте, что медиа-файлы существуют в директории `backend/media/`
4. Убедитесь, что у бэкенда настроена корректная обработка статических и медиа-файлов

