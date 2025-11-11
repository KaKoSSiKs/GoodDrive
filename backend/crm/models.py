from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from django.utils import timezone


class Customer(models.Model):
    """Модель клиента (CRM)"""
    
    CATEGORY_CHOICES = [
        ('new', 'Новый'),
        ('regular', 'Постоянный'),
        ('vip', 'VIP'),
        ('inactive', 'Неактивный'),
    ]
    
    # Основная информация
    name = models.CharField(
        max_length=200,
        verbose_name="Имя"
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Телефон"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )
    
    # Адрес
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Город"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Адрес"
    )
    
    # Категория клиента
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='new',
        verbose_name="Категория"
    )
    
    # Статистика (обновляется автоматически)
    total_orders = models.PositiveIntegerField(
        default=0,
        verbose_name="Всего заказов"
    )
    total_spent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Всего потрачено"
    )
    average_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Средний чек"
    )
    last_order_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата последнего заказа"
    )
    
    # Заметки
    notes = models.TextField(
        blank=True,
        verbose_name="Заметки"
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
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['category']),
            models.Index(fields=['-total_spent']),
            models.Index(fields=['-last_order_date']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.phone})"
    
    def update_statistics(self):
        """Обновить статистику клиента на основе заказов"""
        from orders.models import Order
        
        orders = Order.objects.filter(customer_phone=self.phone, status='completed')
        
        self.total_orders = orders.count()
        self.total_spent = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        self.average_order = orders.aggregate(avg=Avg('total_amount'))['avg'] or 0
        
        last_order = orders.order_by('-created_at').first()
        if last_order:
            self.last_order_date = last_order.created_at
        
        # Автоматическая категоризация
        if self.total_orders == 0:
            self.category = 'new'
        elif self.total_orders >= 10 or self.total_spent >= 100000:
            self.category = 'vip'
        elif self.total_orders >= 3:
            self.category = 'regular'
        elif self.last_order_date and (timezone.now() - self.last_order_date).days > 180:
            self.category = 'inactive'
        
        self.save()
    
    def get_lifetime_value(self):
        """Рассчитать LTV (Lifetime Value) клиента"""
        # Простой расчёт: общая сумма покупок
        return float(self.total_spent)
    
    def get_orders_history(self):
        """Получить историю заказов клиента"""
        from orders.models import Order
        return Order.objects.filter(customer_phone=self.phone).order_by('-created_at')


class CustomerNote(models.Model):
    """Заметка о клиенте"""
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='customer_notes',
        verbose_name="Клиент"
    )
    note = models.TextField(
        verbose_name="Заметка"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customer_notes',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    class Meta:
        verbose_name = "Заметка о клиенте"
        verbose_name_plural = "Заметки о клиентах"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заметка о {self.customer.name}"

