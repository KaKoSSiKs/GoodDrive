"""
Django management команда для автоматической загрузки изображений автозапчастей
Использует бесплатные источники без API ключей

Использование:
    python manage.py fetch_part_images --limit 100
    python manage.py fetch_part_images --part-id 5
"""

from django.core.management.base import BaseCommand
from catalog.models import Part, PartImage
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote_plus


class Command(BaseCommand):
    help = 'Автоматическая загрузка изображений для автозапчастей'

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
        
        self.stdout.write(self.style.SUCCESS('🚀 Начинаем загрузку изображений автозапчастей'))
        
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
        self.stdout.write(f"📦 Найдено товаров для обработки: {total}")
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for index, part in enumerate(parts, 1):
            self.stdout.write(f"\n[{index}/{total}] Обрабатываем: {part.title[:50]}...")
            
            try:
                # Пропускаем, если уже есть изображения и не force
                if not force and part.images.exists():
                    self.stdout.write(self.style.WARNING(f"  ⏭️  Уже есть изображения, пропускаем"))
                    skip_count += 1
                    continue
                
                # Формируем поисковый запрос
                search_query = self.build_search_query(part)
                self.stdout.write(f"  🔍 Поиск: {search_query[:60]}...")
                
                # Пытаемся найти изображение
                image_url = self.search_image(search_query)
                
                if image_url:
                    # Удаляем старые изображения если force
                    if force:
                        part.images.all().delete()
                    
                    # Создаём запись изображения
                    PartImage.objects.create(
                        part=part,
                        image_url=image_url,
                        alt_text=f"{part.brand.name} {part.title}",
                        order_index=0
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f"  ✅ Изображение добавлено"))
                    success_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f"  ⚠️  Изображение не найдено"))
                    error_count += 1
                
                # Задержка чтобы не банили
                time.sleep(0.5)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка: {str(e)}"))
                error_count += 1
                continue
        
        # Итоги
        self.stdout.write(self.style.SUCCESS(f"\n\n✅ Загрузка завершена!"))
        self.stdout.write(f"✅ Успешно: {success_count}")
        self.stdout.write(f"⏭️  Пропущено: {skip_count}")
        self.stdout.write(f"❌ Ошибок: {error_count}")

    def build_search_query(self, part):
        """Формируем оптимальный поисковый запрос"""
        # Берём бренд, артикул и название
        brand = part.brand.name
        article = part.original_number or part.manufacturer_number or ''
        title = part.title
        
        # Очищаем название от лишних символов
        title_clean = re.sub(r'[^\w\s]', ' ', title).strip()
        
        # Формируем запрос
        if article:
            query = f"{brand} {article} {title_clean} автозапчасть"
        else:
            query = f"{brand} {title_clean} автозапчасть"
        
        return query.strip()

    def search_image(self, query):
        """Поиск изображения через DuckDuckGo (бесплатно, без ограничений)"""
        try:
            # DuckDuckGo Image Search
            url = f"https://duckduckgo.com/?q={quote_plus(query)}&iax=images&ia=images"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # Получаем страницу поиска
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Используем vqd token для получения результатов
                vqd_match = re.search(r'vqd="([^"]+)"', response.text)
                if vqd_match:
                    vqd = vqd_match.group(1)
                    
                    # Запрос к API DuckDuckGo для получения изображений
                    api_url = f"https://duckduckgo.com/i.js?q={quote_plus(query)}&o=json&vqd={vqd}"
                    api_response = requests.get(api_url, headers=headers, timeout=10)
                    
                    if api_response.status_code == 200:
                        data = api_response.json()
                        results = data.get('results', [])
                        
                        if results:
                            # Берём первое изображение
                            image_url = results[0].get('image')
                            if image_url and self.is_valid_image_url(image_url):
                                return image_url
            
            # Fallback: Google Images парсинг
            return self.search_image_google(query)
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  DuckDuckGo ошибка: {str(e)}, пробуем Google..."))
            return self.search_image_google(query)

    def search_image_google(self, query):
        """Fallback поиск через Google Images (парсинг HTML)"""
        try:
            url = f"https://www.google.com/search?q={quote_plus(query)}&tbm=isch"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Ищем URL изображений в HTML
                # Google Images встраивает данные в JS скрипты
                image_urls = re.findall(r'"(https://[^"]+\.(?:jpg|jpeg|png|webp))"', response.text)
                
                # Фильтруем служебные URL Google
                for img_url in image_urls:
                    if 'googleusercontent.com' not in img_url and 'gstatic.com' not in img_url:
                        if self.is_valid_image_url(img_url):
                            return img_url
                
                # Если не нашли, берём любую
                if image_urls:
                    return image_urls[0]
            
            return None
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  Google Images ошибка: {str(e)}"))
            return None

    def is_valid_image_url(self, url):
        """Проверка валидности URL изображения"""
        if not url:
            return False
        
        # Проверяем формат
        if not url.startswith('http'):
            return False
        
        # Проверяем расширение
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        if not any(url.lower().endswith(ext) for ext in valid_extensions):
            # Проверяем наличие расширения в query параметрах
            if not any(ext in url.lower() for ext in valid_extensions):
                return False
        
        # Проверяем доступность (опционально, замедляет процесс)
        # try:
        #     response = requests.head(url, timeout=3)
        #     return response.status_code == 200
        # except:
        #     return False
        
        return True

