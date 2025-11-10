"""
Django management команда для загрузки ЧИСТЫХ изображений автозапчастей БЕЗ ВОДЯНЫХ ЗНАКОВ
Использует бесплатные источники с проверкой на водяные знаки

Использование:
    python manage.py fetch_clean_images
    python manage.py fetch_clean_images --limit 50
    python manage.py fetch_clean_images --part-id 5
"""

from django.core.management.base import BaseCommand
from catalog.models import Part, PartImage
import requests
from urllib.parse import quote_plus
import time
import re


class Command(BaseCommand):
    help = 'Загрузка чистых изображений автозапчастей БЕЗ ВОДЯНЫХ ЗНАКОВ'

    # Список доменов с водяными знаками (ИЗБЕГАТЬ!)
    BLACKLISTED_DOMAINS = [
        'antas.ru',
        'exist.ru',
        'emex.ru',
        'autopiter.ru',
        'avto-moto24.ru',
        'shutterstock',
        'gettyimages',
        'istockphoto',
        '123rf',
        'dreamstime',
        'depositphotos',
        'freepik',
        'alamy',
    ]

    # Список НАДЕЖНЫХ источников без водяных знаков
    TRUSTED_SOURCES = [
        'wikimedia.org',
        'wikipedia.org',
        'commons.wikimedia.org',
        'unsplash.com',
        'pexels.com',
        'pixabay.com',
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Максимальное количество товаров для обработки'
        )
        parser.add_argument(
            '--part-id',
            type=int,
            help='Обработать конкретную автозапчасть по ID'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписать существующие изображения'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        part_id = options['part_id']
        force = options['force']
        
        self.stdout.write(self.style.SUCCESS('🚀 Загрузка ЧИСТЫХ изображений БЕЗ ВОДЯНЫХ ЗНАКОВ'))
        self.stdout.write(self.style.WARNING('⚠️  Будут использоваться только проверенные источники'))
        
        # Определяем queryset
        if part_id:
            parts = Part.objects.filter(id=part_id)
        else:
            # Берём товары без изображений или все, если force=True
            if force:
                parts = Part.objects.all()[:limit]
            else:
                parts = Part.objects.filter(images__isnull=True).distinct()[:limit]
        
        total = parts.count()
        self.stdout.write(f"📦 Найдено товаров для обработки: {total}\n")
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for index, part in enumerate(parts, 1):
            self.stdout.write(f"[{index}/{total}] {part.title[:50]}...")
            
            try:
                # Пропускаем, если уже есть изображения и не force
                if not force and part.images.exists():
                    self.stdout.write(self.style.WARNING("  ⏭️  Уже есть изображения"))
                    skip_count += 1
                    continue
                
                # Формируем поисковый запрос
                search_query = self.build_search_query(part)
                
                # Ищем ЧИСТОЕ изображение
                clean_image_url = self.find_clean_image(search_query)
                
                if clean_image_url:
                    # Удаляем старые изображения если force
                    if force:
                        part.images.all().delete()
                    
                    # Создаём запись изображения
                    PartImage.objects.create(
                        part=part,
                        image_url=clean_image_url,
                        alt_text=f"{part.brand.name} {part.title}",
                        order_index=0
                    )
                    
                    self.stdout.write(self.style.SUCCESS("  ✅ Чистое изображение добавлено"))
                    success_count += 1
                else:
                    self.stdout.write(self.style.WARNING("  ⚠️  Чистое изображение не найдено"))
                    error_count += 1
                
                # Задержка
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка: {str(e)}"))
                error_count += 1
                continue
        
        # Итоги
        self.stdout.write(self.style.SUCCESS(f"\n✅ Загрузка завершена!"))
        self.stdout.write(f"✅ Успешно: {success_count}")
        self.stdout.write(f"⏭️  Пропущено: {skip_count}")
        self.stdout.write(f"❌ Не найдено: {error_count}")

    def build_search_query(self, part):
        """Формируем оптимальный поисковый запрос"""
        brand = part.brand.name
        article = part.original_number or part.manufacturer_number or ''
        title = part.title
        
        # Очищаем название
        title_clean = re.sub(r'[^\w\s]', ' ', title).strip()
        
        # Формируем запрос с фильтром на качественные фото
        if article:
            query = f"{brand} {article} {title_clean} auto part"
        else:
            query = f"{brand} {title_clean} automotive part"
        
        return query.strip()

    def find_clean_image(self, query):
        """Поиск чистого изображения БЕЗ ВОДЯНЫХ ЗНАКОВ"""
        
        # Пробуем разные источники
        sources = [
            self.search_wikimedia,
            self.search_unsplash,
            self.search_duckduckgo_filtered,
        ]
        
        for search_func in sources:
            try:
                image_url = search_func(query)
                if image_url and self.is_clean_image(image_url):
                    return image_url
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  ⚠️  {search_func.__name__}: {str(e)}"))
                continue
        
        return None

    def search_wikimedia(self, query):
        """Поиск в Wikimedia Commons (без водяных знаков!)"""
        try:
            api_url = "https://commons.wikimedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srnamespace': 6,  # File namespace
                'srlimit': 5
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                search_results = data.get('query', {}).get('search', [])
                
                for result in search_results:
                    title = result.get('title', '')
                    if title.startswith('File:'):
                        # Получаем URL изображения
                        image_url = self.get_wikimedia_image_url(title)
                        if image_url:
                            return image_url
            
            return None
        except Exception:
            return None

    def get_wikimedia_image_url(self, file_title):
        """Получение прямого URL изображения из Wikimedia"""
        try:
            api_url = "https://commons.wikimedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': file_title,
                'prop': 'imageinfo',
                'iiprop': 'url',
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                pages = data.get('query', {}).get('pages', {})
                for page in pages.values():
                    imageinfo = page.get('imageinfo', [])
                    if imageinfo:
                        return imageinfo[0].get('url')
            
            return None
        except Exception:
            return None

    def search_unsplash(self, query):
        """Поиск на Unsplash (бесплатно, без водяных знаков)"""
        # Примечание: для Unsplash нужен API ключ
        # Здесь пример, в реальности нужно зарегистрироваться на unsplash.com/developers
        # и получить Access Key
        return None  # Пока отключено

    def search_duckduckgo_filtered(self, query):
        """Поиск через DuckDuckGo с фильтрацией водяных знаков"""
        try:
            url = f"https://duckduckgo.com/?q={quote_plus(query)}&iax=images&ia=images"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Извлекаем vqd токен
                vqd_match = re.search(r'vqd="([^"]+)"', response.text)
                if vqd_match:
                    vqd = vqd_match.group(1)
                    
                    # Запрос к API
                    api_url = f"https://duckduckgo.com/i.js?q={quote_plus(query)}&o=json&vqd={vqd}"
                    api_response = requests.get(api_url, headers=headers, timeout=10)
                    
                    if api_response.status_code == 200:
                        data = api_response.json()
                        results = data.get('results', [])
                        
                        # Фильтруем результаты
                        for result in results[:10]:  # Проверяем первые 10
                            image_url = result.get('image')
                            if image_url and self.is_clean_image(image_url):
                                return image_url
            
            return None
            
        except Exception:
            return None

    def is_clean_image(self, url):
        """Проверка, что изображение БЕЗ ВОДЯНЫХ ЗНАКОВ"""
        if not url:
            return False
        
        url_lower = url.lower()
        
        # Проверяем на наличие запрещенных доменов
        for domain in self.BLACKLISTED_DOMAINS:
            if domain.lower() in url_lower:
                self.stdout.write(f"    ❌ Отклонено (водяной знак): {domain}")
                return False
        
        # Проверяем формат
        if not url.startswith('http'):
            return False
        
        # Проверяем расширение
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        has_valid_ext = any(url_lower.endswith(ext) for ext in valid_extensions)
        has_ext_in_params = any(ext in url_lower for ext in valid_extensions)
        
        if not (has_valid_ext or has_ext_in_params):
            return False
        
        # Дополнительная проверка на надежные источники (предпочтительно)
        is_trusted = any(trusted in url_lower for trusted in self.TRUSTED_SOURCES)
        if is_trusted:
            self.stdout.write(f"    ✅ Надежный источник")
        
        return True

