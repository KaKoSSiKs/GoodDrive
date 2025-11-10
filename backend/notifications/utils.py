from .models import Notification
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def create_notification(
    type,
    title,
    message,
    priority='medium',
    link='',
    related_order_id=None,
    related_part_id=None,
    send_email=False
):
    """Создать уведомление"""
    notification = Notification.objects.create(
        type=type,
        title=title,
        message=message,
        priority=priority,
        link=link,
        related_order_id=related_order_id,
        related_part_id=related_part_id
    )
    
    # Отправка email (опционально)
    if send_email:
        try:
            send_notification_email(notification)
            notification.is_sent_email = True
            notification.save()
        except Exception as e:
            logger.error(f"Ошибка отправки email: {e}")
    
    return notification


def send_notification_email(notification):
    """Отправить email уведомление"""
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['89227081553@mail.ru']  # Можно настроить из NotificationSettings
    
    subject = f"[GoodDrive] {notification.title}"
    message = notification.message
    
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def notify_new_order(order):
    """Уведомление о новом заказе"""
    create_notification(
        type='new_order',
        title=f'Новый заказ #{order.order_number}',
        message=f'Клиент: {order.customer_name}\nСумма: {order.total_amount} ₽',
        priority='high',
        link=f'/admin/orders',
        related_order_id=order.id,
        send_email=True
    )


def notify_low_stock(part):
    """Уведомление о низком остатке"""
    create_notification(
        type='low_stock',
        title=f'Низкий остаток: {part.title}',
        message=f'Осталось всего {part.available} шт.',
        priority='medium',
        link=f'/admin/inventory',
        related_part_id=part.id
    )


def notify_zero_stock(part):
    """Уведомление о нулевом остатке"""
    create_notification(
        type='zero_stock',
        title=f'Товар закончился: {part.title}',
        message=f'Необходимо пополнить склад',
        priority='critical',
        link=f'/admin/inventory',
        related_part_id=part.id,
        send_email=True
    )


def check_stuck_orders():
    """Проверка застрявших заказов (>24 часа в одном статусе)"""
    from orders.models import Order
    from django.utils import timezone
    from datetime import timedelta
    
    threshold = timezone.now() - timedelta(hours=24)
    stuck_orders = Order.objects.filter(
        status__in=['new', 'processing'],
        updated_at__lt=threshold
    )
    
    for order in stuck_orders:
        create_notification(
            type='stuck_order',
            title=f'Заказ завис: #{order.order_number}',
            message=f'Заказ в статусе "{order.get_status_display()}" более 24 часов',
            priority='high',
            link=f'/admin/orders',
            related_order_id=order.id
        )

