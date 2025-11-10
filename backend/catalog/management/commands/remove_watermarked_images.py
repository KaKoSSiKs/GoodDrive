"""
Django management команда для удаления изображений с водяными знаками

Использование:
    python manage.py remove_watermarked_images
    python manage.py remove_watermarked_images --dry-run  # Только показать, не удалять
"""

from django.core.management.base import BaseCommand
from catalog.models import PartImage
import re


class Command(BaseCommand):
    help = 'Удаление изображений с водяными знаками (antas.ru и другие)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только показать изображения с водяными знаками, не удалять'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 РЕЖИМ ПРЕДПРОСМОТРА (изображения не будут удалены)'))
        else:
            self.stdout.write(self.style.SUCCESS('🚀 Начинаем удаление изображений с водяными знаками'))
        
        # Список доменов с водяными знаками
        watermark_domains = [
            'antas.ru',
            'exist.ru',
            'emex.ru',
            'autopiter.ru',
            'avto-moto24.ru',
            'auto.ru',
            'avito.ru',
            'shutterstock',
            'gettyimages',
            'istockphoto',
            '123rf',
            'dreamstime',
            'depositphotos',
            'freepik',
        ]
        
        # Получаем все изображения
        all_images = PartImage.objects.all()
        total = all_images.count()
        
        self.stdout.write(f"📦 Всего изображений в базе: {total}")
        
        watermarked_images = []
        
        # Проверяем каждое изображение
        for image in all_images:
            image_url = image.image_url or ''
            
            # Проверяем URL на наличие водяных знаков
            for domain in watermark_domains:
                if domain.lower() in image_url.lower():
                    watermarked_images.append({
                        'image': image,
                        'domain': domain,
                        'part_title': image.part.title if image.part else 'Unknown'
                    })
                    break
        
        if not watermarked_images:
            self.stdout.write(self.style.SUCCESS('\n✅ Изображений с водяными знаками не найдено!'))
            return
        
        # Выводим список найденных изображений
        self.stdout.write(f"\n⚠️  Найдено изображений с водяными знаками: {len(watermarked_images)}\n")
        
        for idx, item in enumerate(watermarked_images, 1):
            image = item['image']
            domain = item['domain']
            part_title = item['part_title']
            
            self.stdout.write(
                f"  {idx}. [{domain}] {part_title[:60]}...\n"
                f"     URL: {image.image_url[:80]}..."
            )
        
        # Удаляем или показываем предупреждение
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"\n\n⚠️  В режиме предпросмотра. Для удаления запустите без --dry-run:\n"
                    f"python manage.py remove_watermarked_images"
                )
            )
        else:
            # Подтверждение
            self.stdout.write(
                self.style.WARNING(
                    f"\n\n⚠️  ВНИМАНИЕ! Будет удалено {len(watermarked_images)} изображений."
                )
            )
            
            # Удаляем
            deleted_count = 0
            for item in watermarked_images:
                try:
                    item['image'].delete()
                    deleted_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"  ❌ Ошибка при удалении: {str(e)}")
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✅ Удалено изображений с водяными знаками: {deleted_count}"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f"\n💡 Для загрузки новых изображений без водяных знаков запустите:\n"
                    f"python manage.py fetch_clean_images"
                )
            )

