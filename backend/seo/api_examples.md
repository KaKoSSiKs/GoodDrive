# Примеры использования SEO API для GoodDrive

## 1. Получение SEO метаданных для страницы

### Запрос:
```
GET /api/seo/meta/home/
```

### Ответ:
```json
{
    "slug": "home",
    "title": "GoodDrive - Интернет-магазин автозапчастей",
    "description": "Широкий выбор автозапчастей от ведущих производителей. Быстрая доставка по всей России. Гарантия качества.",
    "keywords": "автозапчасти, запчасти для авто, интернет-магазин, доставка",
    "og_title": "GoodDrive - Интернет-магазин автозапчастей",
    "og_description": "Широкий выбор автозапчастей от ведущих производителей. Быстрая доставка по всей России.",
    "og_image_url": "https://example.com/media/seo/og_images/home_og.jpg",
    "canonical_url": "https://gooddrive.ru/",
    "robots": "index, follow",
    "yandex_verification": "abc123def456",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T16:45:00Z"
}
```

## 2. Получение глобальных SEO настроек

### Запрос:
```
GET /api/seo/settings/
```

### Ответ:
```json
{
    "site_name": "GoodDrive",
    "site_description": "Интернет-магазин автозапчастей GoodDrive",
    "default_og_image_url": "https://example.com/media/seo/default/default_og.jpg",
    "yandex_verification": "abc123def456",
    "google_verification": "xyz789uvw012",
    "yandex_metrica": "12345678",
    "google_analytics": "G-ABCDEFGHIJ",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T16:45:00Z"
}
```

## 3. Создание новой SEO страницы

### Запрос:
```
POST /api/seo/pages/
Content-Type: application/json

{
    "slug": "catalog",
    "title": "Каталог автозапчастей - GoodDrive",
    "description": "Полный каталог автозапчастей от ведущих производителей. Фильтры по бренду, цене, наличию.",
    "keywords": "каталог, автозапчасти, фильтры, бренды",
    "og_title": "Каталог автозапчастей - GoodDrive",
    "og_description": "Полный каталог автозапчастей от ведущих производителей",
    "og_image": "https://example.com/media/seo/og_images/catalog_og.jpg",
    "canonical_url": "https://gooddrive.ru/catalog/",
    "robots": "index, follow",
    "is_active": true
}
```

### Ответ:
```json
{
    "slug": "catalog",
    "title": "Каталог автозапчастей - GoodDrive",
    "description": "Полный каталог автозапчастей от ведущих производителей. Фильтры по бренду, цене, наличию.",
    "keywords": "каталог, автозапчасти, фильтры, бренды",
    "og_title": "Каталог автозапчастей - GoodDrive",
    "og_description": "Полный каталог автозапчастей от ведущих производителей",
    "og_image_url": "https://example.com/media/seo/og_images/catalog_og.jpg",
    "canonical_url": "https://gooddrive.ru/catalog/",
    "robots": "index, follow",
    "yandex_verification": "",
    "is_active": true,
    "created_at": "2024-01-21T14:20:00Z",
    "updated_at": "2024-01-21T14:20:00Z"
}
```

## 4. Обновление SEO настроек

### Запрос:
```
PUT /api/seo/settings/1/
Content-Type: application/json

{
    "site_name": "GoodDrive - Автозапчасти",
    "site_description": "Интернет-магазин автозапчастей GoodDrive. Широкий выбор, быстрая доставка.",
    "yandex_verification": "new_verification_code",
    "google_verification": "new_google_code",
    "yandex_metrica": "87654321",
    "google_analytics": "G-ZYXWVUTSRQ"
}
```

## 5. Получение robots.txt

### Запрос:
```
GET /robots.txt
```

### Ответ:
```
User-agent: *
Allow: /

User-agent: Yandex
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: https://gooddrive.ru/sitemap.xml
```

## 6. Получение sitemap.xml

### Запрос:
```
GET /sitemap.xml
```

### Ответ:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://gooddrive.ru/</loc>
        <lastmod>2024-01-21</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://gooddrive.ru/catalog/</loc>
        <lastmod>2024-01-21</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://gooddrive.ru/catalog/part/1/</loc>
        <lastmod>2024-01-20</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <!-- ... другие страницы ... -->
</urlset>
```

## 7. Страница подтверждения Яндекс.Вебмастер

### Запрос:
```
GET /yandex-verification.html
```

### Ответ:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Подтверждение Яндекс.Вебмастер</title>
</head>
<body>
    <p>Код подтверждения: abc123def456</p>
</body>
</html>
```

## Интеграция с фронтендом

### Пример использования в SvelteKit:

```javascript
// Получение SEO метаданных для страницы
export async function load({ params }) {
    const response = await fetch('/api/seo/meta/home/');
    const seoData = await response.json();
    
    return {
        seo: seoData
    };
}

// В компоненте
<script>
    export let seo;
</script>

<svelte:head>
    <title>{seo.title}</title>
    <meta name="description" content={seo.description} />
    <meta name="keywords" content={seo.keywords} />
    <meta name="robots" content={seo.robots} />
    
    <!-- Open Graph -->
    <meta property="og:title" content={seo.og_title} />
    <meta property="og:description" content={seo.og_description} />
    <meta property="og:image" content={seo.og_image_url} />
    <meta property="og:type" content="website" />
    
    <!-- Canonical URL -->
    {#if seo.canonical_url}
        <link rel="canonical" href={seo.canonical_url} />
    {/if}
    
    <!-- Яндекс.Вебмастер -->
    {#if seo.yandex_verification}
        <meta name="yandex-verification" content={seo.yandex_verification} />
    {/if}
</svelte:head>
```

## Структура медиа-файлов

```
media/
├── parts/                    # Изображения автозапчастей
│   ├── 1/                   # ID автозапчасти
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   └── 2/
│       └── image1.jpg
├── seo/                     # SEO изображения
│   ├── og_images/           # Open Graph изображения
│   │   ├── home_og.jpg
│   │   └── catalog_og.jpg
│   └── default/             # Изображения по умолчанию
│       └── default_og.jpg
└── files/                   # Другие файлы
    └── documents/
```

## Настройка в Django Admin

1. **SEO страницы** (`/admin/seo/seopage/`):
   - Создание и редактирование метаданных для каждой страницы
   - Загрузка изображений для Open Graph
   - Настройка канонических URL

2. **SEO настройки** (`/admin/seo/seosettings/`):
   - Глобальные настройки сайта
   - Коды подтверждения поисковых систем
   - ID счетчиков аналитики

3. **Изображения автозапчастей** (`/admin/catalog/partimage/`):
   - Загрузка изображений через файловое поле
   - Превью изображений в админке
   - Автоматическая генерация URL

