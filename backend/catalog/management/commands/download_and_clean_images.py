"""
Django management команда для скачивания изображений из интернета
и удаления водяных знаков с помощью Python

Использование:
    python manage.py download_and_clean_images
    python manage.py download_and_clean_images --limit 50
    python manage.py download_and_clean_images --part-id 5
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from catalog.models import Part, PartImage
import requests
from PIL import Image, ImageFilter, ImageDraw
import io
import os
from urllib.parse import urlparse
import hashlib
import time
import numpy as np


class Command(BaseCommand):
    help = 'Скачивает изображения из интернета локально и пытается удалить водяные знаки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Максимальное количество изображений для обработки'
        )
        parser.add_argument(
            '--part-id',
            type=int,
            help='Обработать изображения конкретной автозапчасти по ID'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписать существующие локальные изображения'
        )
        parser.add_argument(
            '--method',
            type=str,
            default='crop',
            choices=['crop', 'blur', 'inpaint', 'all'],
            help='Метод удаления водяных знаков'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        part_id = options['part_id']
        force = options['force']
        method = options['method']
        
        self.stdout.write(self.style.SUCCESS('🚀 Скачивание и очистка изображений от водяных знаков'))
        
        # Определяем queryset
        if part_id:
            images = PartImage.objects.filter(part_id=part_id)
        else:
            # Берём изображения с внешними URL (не локальные)
            images = PartImage.objects.filter(
                image_url__startswith='http'
            ).exclude(
                image_url__icontains='/media/'
            )[:limit]
        
        total = images.count()
        self.stdout.write(f"📦 Найдено изображений для обработки: {total}\n")
        
        if total == 0:
            self.stdout.write(self.style.WARNING('✅ Все изображения уже локальные или нет изображений'))
            return
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for index, image_obj in enumerate(images, 1):
            try:
                part_title = image_obj.part.title if image_obj.part else 'Unknown'
                self.stdout.write(f"\n[{index}/{total}] {part_title[:50]}...")
                self.stdout.write(f"  URL: {image_obj.image_url[:80]}...")
                
                # Скачиваем изображение
                self.stdout.write("  📥 Скачивание...")
                img_data = self.download_image(image_obj.image_url)
                
                if not img_data:
                    self.stdout.write(self.style.ERROR("  ❌ Не удалось скачать"))
                    error_count += 1
                    continue
                
                # Открываем изображение с помощью PIL
                img = Image.open(io.BytesIO(img_data))
                
                # Конвертируем в RGB если нужно
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                self.stdout.write(f"  🖼️  Размер: {img.size}")
                
                # Пытаемся удалить водяной знак
                self.stdout.write(f"  🧹 Удаление водяных знаков (метод: {method})...")
                
                if method == 'crop':
                    cleaned_img = self.remove_watermark_crop(img)
                elif method == 'blur':
                    cleaned_img = self.remove_watermark_blur(img)
                elif method == 'inpaint':
                    cleaned_img = self.remove_watermark_inpaint(img)
                elif method == 'all':
                    # Пробуем все методы
                    cleaned_img = self.remove_watermark_auto(img)
                else:
                    cleaned_img = img
                
                # Сохраняем локально
                filename = self.generate_filename(image_obj)
                
                # Конвертируем обратно в байты
                output = io.BytesIO()
                cleaned_img.save(output, format='JPEG', quality=95)
                output.seek(0)
                
                # Сохраняем в Django media
                image_obj.image.save(
                    filename,
                    ContentFile(output.read()),
                    save=False
                )
                
                # Обновляем URL на локальный путь
                local_url = f"/media/{image_obj.image.name}"
                image_obj.image_url = local_url
                image_obj.save()
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ Сохранено: {local_url}"))
                success_count += 1
                
                # Задержка
                time.sleep(0.3)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка: {str(e)}"))
                error_count += 1
                continue
        
        # Итоги
        self.stdout.write(self.style.SUCCESS(f"\n\n✅ Обработка завершена!"))
        self.stdout.write(f"✅ Успешно: {success_count}")
        self.stdout.write(f"⏭️  Пропущено: {skip_count}")
        self.stdout.write(f"❌ Ошибок: {error_count}")

    def download_image(self, url):
        """Скачивает изображение по URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                return response.content
            
            return None
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  ⚠️  Ошибка скачивания: {str(e)}"))
            return None

    def remove_watermark_crop(self, img):
        """
        Метод 1: Обрезка краёв (где обычно находятся водяные знаки)
        Удаляет 10% от каждого края
        """
        width, height = img.size
        
        # Обрезаем 5% снизу (где обычно водяные знаки)
        crop_bottom = int(height * 0.05)
        
        # Обрезаем 3% справа
        crop_right = int(width * 0.03)
        
        # Новые размеры
        new_box = (0, 0, width - crop_right, height - crop_bottom)
        
        return img.crop(new_box)

    def remove_watermark_blur(self, img):
        """
        Метод 2: Размытие области с водяным знаком
        Размывает нижнюю часть изображения
        """
        width, height = img.size
        
        # Создаём копию
        result = img.copy()
        
        # Область водяного знака (нижние 15%)
        watermark_area = (0, int(height * 0.85), width, height)
        
        # Вырезаем область
        region = img.crop(watermark_area)
        
        # Сильно размываем
        blurred = region.filter(ImageFilter.GaussianBlur(radius=20))
        
        # Вставляем обратно
        result.paste(blurred, watermark_area)
        
        return result

    def remove_watermark_inpaint(self, img):
        """
        Метод 3: "Закрашивание" водяного знака соседними пикселями
        Простая версия inpainting
        """
        width, height = img.size
        
        # Создаём копию
        result = img.copy()
        pixels = result.load()
        
        # Область водяного знака (нижние 10%)
        watermark_top = int(height * 0.90)
        
        # Для каждого пикселя в области водяного знака
        # берём цвет из области выше
        for y in range(watermark_top, height):
            for x in range(width):
                # Берём пиксель на 50px выше
                source_y = max(0, y - 50)
                pixels[x, y] = pixels[x, source_y]
        
        return result

    def remove_watermark_auto(self, img):
        """
        Автоматический выбор метода
        Пробует разные подходы
        """
        # Сначала обрезаем
        img = self.remove_watermark_crop(img)
        
        # Потом размываем остатки
        img = self.remove_watermark_blur(img)
        
        return img

    def generate_filename(self, image_obj):
        """Генерирует уникальное имя файла"""
        part_id = image_obj.part.id if image_obj.part else 'unknown'
        
        # Хэш от URL для уникальности
        url_hash = hashlib.md5(image_obj.image_url.encode()).hexdigest()[:8]
        
        filename = f"part_{part_id}_{url_hash}_clean.jpg"
        
        return filename

