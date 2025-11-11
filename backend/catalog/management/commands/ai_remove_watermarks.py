"""
Продвинутая команда для удаления водяных знаков с помощью OpenCV и AI

Требует: pip install opencv-python opencv-contrib-python

Использование:
    python manage.py ai_remove_watermarks
    python manage.py ai_remove_watermarks --limit 20
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from catalog.models import Part, PartImage
import requests
from PIL import Image
import io
import time
import hashlib

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class Command(BaseCommand):
    help = 'Удаление водяных знаков с помощью OpenCV (AI инструменты)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Максимальное количество изображений'
        )
        parser.add_argument(
            '--part-id',
            type=int,
            help='Обработать конкретную автозапчасть'
        )

    def handle(self, *args, **options):
        if not HAS_OPENCV:
            self.stdout.write(
                self.style.ERROR(
                    '❌ OpenCV не установлен!\n'
                    'Установите: pip install opencv-python opencv-contrib-python numpy'
                )
            )
            return
        
        limit = options['limit']
        part_id = options['part_id']
        
        self.stdout.write(self.style.SUCCESS('🤖 AI удаление водяных знаков с OpenCV'))
        
        # Получаем изображения
        if part_id:
            images = PartImage.objects.filter(part_id=part_id)
        else:
            images = PartImage.objects.filter(
                image_url__startswith='http'
            ).exclude(
                image_url__icontains='/media/'
            )[:limit]
        
        total = images.count()
        self.stdout.write(f"📦 Изображений для обработки: {total}\n")
        
        if total == 0:
            self.stdout.write(self.style.WARNING('✅ Все изображения уже локальные'))
            return
        
        success = 0
        errors = 0
        
        for index, img_obj in enumerate(images, 1):
            try:
                part_title = img_obj.part.title if img_obj.part else 'Unknown'
                self.stdout.write(f"\n[{index}/{total}] {part_title[:50]}...")
                
                # Скачиваем
                self.stdout.write("  📥 Скачивание...")
                img_data = self.download_image(img_obj.image_url)
                
                if not img_data:
                    self.stdout.write(self.style.ERROR("  ❌ Не удалось скачать"))
                    errors += 1
                    continue
                
                # Конвертируем в OpenCV формат
                nparr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is None:
                    self.stdout.write(self.style.ERROR("  ❌ Не удалось декодировать"))
                    errors += 1
                    continue
                
                self.stdout.write(f"  🖼️  Размер: {img.shape}")
                
                # Применяем AI удаление водяных знаков
                self.stdout.write("  🤖 AI обработка...")
                cleaned_img = self.remove_watermark_ai(img)
                
                # Сохраняем
                filename = self.generate_filename(img_obj)
                
                # Конвертируем обратно в JPEG
                success_encode, buffer = cv2.imencode('.jpg', cleaned_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
                
                if not success_encode:
                    self.stdout.write(self.style.ERROR("  ❌ Ошибка кодирования"))
                    errors += 1
                    continue
                
                # Сохраняем в Django
                img_obj.image.save(
                    filename,
                    ContentFile(buffer.tobytes()),
                    save=False
                )
                
                # Обновляем URL
                local_url = f"/media/{img_obj.image.name}"
                img_obj.image_url = local_url
                img_obj.save()
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ Готово: {local_url}"))
                success += 1
                
                time.sleep(0.3)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка: {str(e)}"))
                errors += 1
                continue
        
        # Итоги
        self.stdout.write(self.style.SUCCESS(f"\n\n✅ Завершено!"))
        self.stdout.write(f"✅ Успешно: {success}")
        self.stdout.write(f"❌ Ошибок: {errors}")

    def download_image(self, url):
        """Скачивает изображение"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                return response.content
            
            return None
        except Exception:
            return None

    def remove_watermark_ai(self, img):
        """
        AI удаление водяных знаков с помощью OpenCV
        Использует несколько техник компьютерного зрения
        """
        
        # Метод 1: Детекция текста и его удаление
        img = self.remove_text_watermarks(img)
        
        # Метод 2: Inpainting (закрашивание)
        img = self.apply_inpainting(img)
        
        # Метод 3: Обрезка краёв
        img = self.smart_crop(img)
        
        return img

    def remove_text_watermarks(self, img):
        """
        Детектирует текстовые водяные знаки и удаляет их
        """
        height, width = img.shape[:2]
        
        # Конвертируем в серый
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Пороговая обработка для выделения текста
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Находим контуры (потенциальные водяные знаки)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Создаём маску для водяных знаков
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        
        # Область водяного знака (обычно внизу)
        watermark_zone = height * 0.80
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Если контур в нижней части - это вероятно водяной знак
            if y > watermark_zone and w > 50 and h > 10:
                # Расширяем область немного
                cv2.rectangle(mask, (x-2, y-2), (x+w+2, y+h+2), 255, -1)
        
        # Применяем inpainting только к маске
        if np.any(mask > 0):
            img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        
        return img

    def apply_inpainting(self, img):
        """
        Продвинутый inpainting для удаления водяных знаков
        """
        height, width = img.shape[:2]
        
        # Создаём маску для нижней части (где обычно водяные знаки)
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        
        # Закрашиваем нижние 8% изображения
        watermark_start = int(height * 0.92)
        mask[watermark_start:, :] = 255
        
        # Применяем Telea inpainting algorithm
        result = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)
        
        return result

    def smart_crop(self, img):
        """
        Умная обрезка: сохраняет главный объект, удаляет края с водяными знаками
        """
        height, width = img.shape[:2]
        
        # Обрезаем нижние 5% (водяные знаки)
        crop_bottom = int(height * 0.05)
        
        # Обрезаем правые 3%
        crop_right = int(width * 0.03)
        
        # Новое изображение
        cropped = img[0:height-crop_bottom, 0:width-crop_right]
        
        return cropped

    def generate_filename(self, image_obj):
        """Генерирует имя файла"""
        part_id = image_obj.part.id if image_obj.part else 'unknown'
        url_hash = hashlib.md5(image_obj.image_url.encode()).hexdigest()[:8]
        return f"part_{part_id}_{url_hash}_ai_clean.jpg"


