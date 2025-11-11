from django.core.management.base import BaseCommand
from django.db import transaction
from crm.models import Customer
from orders.models import Order
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Синхронизировать данные CRM из заказов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update-stats-only',
            action='store_true',
            help='Только обновить статистику существующих клиентов',
        )
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Принудительно обновить данные всех существующих клиентов',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Начало синхронизации CRM...'))
        
        update_stats_only = options['update_stats_only']
        force_update = options['force_update']
        
        if update_stats_only:
            self.update_statistics_only()
        else:
            self.sync_customers(force_update)
        
        self.stdout.write(self.style.SUCCESS('Синхронизация завершена!'))

    def sync_customers(self, force_update=False):
        """Синхронизировать клиентов из заказов"""
        # Получаем уникальные телефоны из заказов
        unique_phones = Order.objects.exclude(
            customer_phone__isnull=True
        ).exclude(
            customer_phone=''
        ).values_list('customer_phone', flat=True).distinct()
        
        created_count = 0
        updated_count = 0
        error_count = 0
        
        total_phones = len(unique_phones)
        self.stdout.write(f'Найдено уникальных телефонов: {total_phones}')
        
        for index, phone in enumerate(unique_phones, 1):
            try:
                # Получаем последний заказ клиента для актуальных данных
                latest_order = Order.objects.filter(
                    customer_phone=phone
                ).order_by('-created_at').first()
                
                if not latest_order:
                    continue
                
                with transaction.atomic():
                    # Создаем или обновляем клиента
                    customer, created = Customer.objects.get_or_create(
                        phone=phone,
                        defaults={
                            'name': latest_order.customer_name or 'Без имени',
                            'email': latest_order.customer_email or '',
                            'city': latest_order.delivery_city or ''
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'[{index}/{total_phones}] Создан: {phone}')
                        )
                    else:
                        # Обновляем данные существующего клиента
                        if force_update:
                            updated = False
                            if latest_order.customer_name and customer.name != latest_order.customer_name:
                                customer.name = latest_order.customer_name
                                updated = True
                            if latest_order.customer_email and customer.email != latest_order.customer_email:
                                customer.email = latest_order.customer_email
                                updated = True
                            if latest_order.delivery_city and customer.city != latest_order.delivery_city:
                                customer.city = latest_order.delivery_city
                                updated = True
                            
                            if updated:
                                customer.save()
                                updated_count += 1
                                self.stdout.write(
                                    self.style.WARNING(f'[{index}/{total_phones}] Обновлен: {phone}')
                                )
                        else:
                            self.stdout.write(f'[{index}/{total_phones}] Пропущен: {phone}')
                    
                    # Обновляем статистику клиента
                    customer.update_statistics()
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'[{index}/{total_phones}] Ошибка для {phone}: {str(e)}')
                )
                logger.error(f"Ошибка синхронизации клиента {phone}: {str(e)}")
                continue
        
        # Итоговая статистика
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'Создано новых клиентов: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Обновлено клиентов: {updated_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Ошибок: {error_count}'))
        self.stdout.write(self.style.SUCCESS(f'Всего клиентов в CRM: {Customer.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

    def update_statistics_only(self):
        """Обновить только статистику существующих клиентов"""
        customers = Customer.objects.all()
        total_customers = customers.count()
        
        self.stdout.write(f'Обновление статистики для {total_customers} клиентов...')
        
        success_count = 0
        error_count = 0
        
        for index, customer in enumerate(customers, 1):
            try:
                customer.update_statistics()
                success_count += 1
                if index % 10 == 0:
                    self.stdout.write(f'Обработано: {index}/{total_customers}')
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'Ошибка для {customer.phone}: {str(e)}')
                )
                logger.error(f"Ошибка обновления статистики для {customer.phone}: {str(e)}")
        
        # Итоговая статистика
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'Успешно обновлено: {success_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Ошибок: {error_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

