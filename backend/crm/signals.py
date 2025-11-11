from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from .models import Customer
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def sync_customer_on_order_save(sender, instance, created, **kwargs):
    """
    Автоматическая синхронизация клиента при создании или обновлении заказа
    """
    if not instance.customer_phone:
        return
    
    try:
        # Создаем или обновляем клиента
        customer, customer_created = Customer.objects.get_or_create(
            phone=instance.customer_phone,
            defaults={
                'name': instance.customer_name or 'Без имени',
                'email': instance.customer_email or '',
                'city': instance.delivery_city or ''
            }
        )
        
        if customer_created:
            logger.info(f"Автоматически создан клиент CRM: {instance.customer_phone}")
        else:
            # Обновляем данные клиента, если они изменились
            updated = False
            
            if instance.customer_name and customer.name != instance.customer_name:
                # Обновляем имя только если оно не было "Без имени"
                if customer.name == 'Без имени' or not customer.name:
                    customer.name = instance.customer_name
                    updated = True
            
            if instance.customer_email and not customer.email:
                # Обновляем email только если он был пустым
                customer.email = instance.customer_email
                updated = True
            
            if instance.delivery_city and not customer.city:
                # Обновляем город только если он был пустым
                customer.city = instance.delivery_city
                updated = True
            
            if updated:
                customer.save()
                logger.info(f"Обновлены данные клиента CRM: {instance.customer_phone}")
        
        # Обновляем статистику клиента
        customer.update_statistics()
        
    except Exception as e:
        logger.error(f"Ошибка автоматической синхронизации CRM для заказа {instance.order_number}: {str(e)}")

