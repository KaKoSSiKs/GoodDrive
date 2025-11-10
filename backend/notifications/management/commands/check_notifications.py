from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from notifications.utils import (
    create_notification,
    notify_low_stock,
    notify_zero_stock,
    check_stuck_orders
)
from catalog.models import Part


class Command(BaseCommand):
    help = 'Проверка товаров с низким остатком и застрявших заказов'

    def handle(self, *args, **kwargs):
        self.stdout.write('Проверка товаров с низким остатком...')
        
        # Товары с нулевым остатком
        zero_stock_parts = Part.objects.filter(available=0)
        for part in zero_stock_parts:
            notify_zero_stock(part)
        self.stdout.write(f'  Найдено товаров с нулевым остатком: {zero_stock_parts.count()}')
        
        # Товары с низким остатком (1-5 шт)
        low_stock_parts = Part.objects.filter(available__gt=0, available__lte=5)
        for part in low_stock_parts:
            notify_low_stock(part)
        self.stdout.write(f'  Найдено товаров с низким остатком: {low_stock_parts.count()}')
        
        # Застрявшие заказы
        self.stdout.write('Проверка застрявших заказов...')
        check_stuck_orders()
        
        self.stdout.write(self.style.SUCCESS('Проверка завершена'))

