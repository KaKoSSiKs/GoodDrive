"""
Management command для импорта автозапчастей из CSV файла
Проще в использовании чем Excel, работает быстрее
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Brand, Warehouse, Part, PartImage
import csv
import os
from decimal import Decimal, InvalidOperation


class Command(BaseCommand):
    help = 'Импортирует автозапчасти из CSV файла'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к CSV файлу')
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Максимальное количество запчастей для импорта'
        )
    
    def handle(self, *args, **options):
        file_path = options['file_path']
        limit = options['limit']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Начинаем импорт из файла: {file_path}'))
        
        # Счетчики
        brands_created = 0
        warehouses_created = 0
        parts_created = 0
        images_created = 0
        errors = []
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            
            with transaction.atomic():
                for row_num, row in enumerate(reader, start=2):
                    if row_num > limit + 1:
                        break
                    
                    try:
                        # Получаем данные из строки (по русским названиям колонок)
                        title = row.get('Наименование полное', '').strip()
                        if not title:
                            continue
                        
                        # Получаем или создаем бренд
                        brand_name = row.get('Фирма производитель', 'Неизвестный').strip()
                        brand, created = Brand.objects.get_or_create(
                            name=brand_name,
                            defaults={'country': ''}
                        )
                        if created:
                            brands_created += 1
                        
                        # Получаем или создаем склад
                        warehouse_name = row.get('Склад / раздел', 'Основной склад').strip()
                        warehouse, created = Warehouse.objects.get_or_create(
                            name=warehouse_name,
                            defaults={'address': 'Не указан'}
                        )
                        if created:
                            warehouses_created += 1
                        
                        # Парсим цены (заменяем запятую на точку)
                        price_str = str(row.get('опт интернет', '0')).replace(',', '.')
                        price = self.parse_decimal(price_str, 0)
                        
                        # Создаем автозапчасть
                        part, created = Part.objects.get_or_create(
                            title=title,
                            brand=brand,
                            defaults={
                                'label': row.get('Метка', '').strip(),
                                'original_number': row.get('Оригинальный номер', '').strip(),
                                'manufacturer_number': row.get('Номер производителя', '').strip(),
                                'warehouse': warehouse,
                                'quantity': self.parse_int(row.get('Количество', 0)),
                                'stock': self.parse_int(row.get('Остаток', 0)),
                                'reserve': self.parse_int(row.get('Резерв', 0)),
                                'available': max(0, self.parse_int(row.get('Доступно', 0))),
                                'price_opt': price,
                                'description': '',
                                'is_active': True
                            }
                        )
                        
                        if created:
                            parts_created += 1
                            
                            # Создаем заглушку для изображения
                            PartImage.objects.create(
                                part=part,
                                image_url='https://via.placeholder.com/600x600/2563EB/FFFFFF?text=Auto+Part',
                                alt_text=title,
                                order_index=0
                            )
                            images_created += 1
                        
                        if row_num % 10 == 0:
                            self.stdout.write(f'Обработано строк: {row_num}')
                        
                    except Exception as e:
                        error_msg = f'Ошибка в строке {row_num}: {str(e)}'
                        errors.append(error_msg)
                        if len(errors) <= 10:  # Показываем первые 10 ошибок
                            self.stdout.write(self.style.ERROR(error_msg))
        
        # Выводим статистику
        self.stdout.write(self.style.SUCCESS('\n✅ Импорт завершен!'))
        self.stdout.write(self.style.SUCCESS(f'📦 Брендов создано: {brands_created}'))
        self.stdout.write(self.style.SUCCESS(f'🏢 Складов создано: {warehouses_created}'))
        self.stdout.write(self.style.SUCCESS(f'🔧 Автозапчастей создано: {parts_created}'))
        self.stdout.write(self.style.SUCCESS(f'🖼️ Изображений создано: {images_created}'))
        
        if errors:
            self.stdout.write(self.style.ERROR(f'\n⚠️ Всего ошибок: {len(errors)}'))
    
    def parse_int(self, value, default=0):
        """Преобразует значение в integer"""
        if value is None or value == '':
            return default
        try:
            if isinstance(value, (int, float)):
                return int(value)
            return int(str(value).strip())
        except (ValueError, AttributeError):
            return default
    
    def parse_decimal(self, value, default=0):
        """Преобразует значение в Decimal"""
        if value is None or value == '':
            return default
        try:
            if isinstance(value, Decimal):
                return value
            return Decimal(str(value).strip().replace(',', '.'))
        except (ValueError, InvalidOperation):
            return default
