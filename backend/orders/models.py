from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid


class Order(models.Model):
    """Модель заказа"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    # Уникальный номер заказа
    order_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Номер заказа",
        help_text="Уникальный номер заказа"
    )
    
    # Контактная информация
    customer_name = models.CharField(
        max_length=100,
        verbose_name="Имя клиента"
    )
    customer_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^[\+]?[1-9][\d]{0,15}$',
            message='Введите корректный номер телефона'
        )],
        verbose_name="Телефон"
    )
    customer_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )
    
    # Адрес доставки
    delivery_address = models.TextField(
        verbose_name="Адрес доставки"
    )
    delivery_city = models.CharField(
        max_length=100,
        verbose_name="Город"
    )
    delivery_postal_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Почтовый индекс"
    )
    
    # Информация о заказе
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая сумма"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа"
    )
    
    # Дополнительная информация
    notes = models.TextField(
        blank=True,
        verbose_name="Комментарии к заказу"
    )
    
    # Временные метки
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer_phone']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Заказ #{self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Генерируем уникальный номер заказа
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_order_number():
        """Генерирует уникальный номер заказа"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"GD{timestamp}{unique_id}"


class OrderItem(models.Model):
    """Модель позиции заказа"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    part = models.ForeignKey(
        'catalog.Part',
        on_delete=models.CASCADE,
        verbose_name="Автозапчасть"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за единицу"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая цена"
    )
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.part.title} x{self.quantity}"
    
    def save(self, *args, **kwargs):
        # Автоматически вычисляем общую цену
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """Модель истории статусов заказа"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name="Заказ"
    )
    status = models.CharField(
        max_length=20,
        choices=Order.STATUS_CHOICES,
        verbose_name="Статус"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата изменения"
    )
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Изменил"
    )
    
    class Meta:
        verbose_name = "История статуса заказа"
        verbose_name_plural = "История статусов заказов"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"








