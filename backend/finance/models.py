from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class ExpenseCategory(models.Model):
    """Категория расходов"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )
    
    class Meta:
        verbose_name = "Категория расходов"
        verbose_name_plural = "Категории расходов"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Expense(models.Model):
    """Модель расхода"""
    
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name='expenses',
        verbose_name="Категория"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Сумма"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    date = models.DateField(
        verbose_name="Дата"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        verbose_name="Создал"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['category', '-date']),
            models.Index(fields=['-date']),
        ]
    
    def __str__(self):
        return f"{self.category.name} - {self.amount} ₽ ({self.date})"


class CashTransaction(models.Model):
    """Модель денежной транзакции (касса)"""
    
    TYPE_CHOICES = [
        ('income', 'Приход'),
        ('expense', 'Расход'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('bank_transfer', 'Банковский перевод'),
        ('online', 'Онлайн-оплата'),
    ]
    
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Тип"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Сумма"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        verbose_name="Способ оплаты"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    
    # Связь с заказом (если транзакция связана с заказом)
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cash_transactions',
        verbose_name="Заказ"
    )
    
    # Связь с расходом (если транзакция - это расход)
    expense = models.ForeignKey(
        Expense,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cash_transactions',
        verbose_name="Расход"
    )
    
    date = models.DateTimeField(
        verbose_name="Дата и время"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cash_transactions',
        verbose_name="Создал"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания записи"
    )
    
    class Meta:
        verbose_name = "Денежная транзакция"
        verbose_name_plural = "Денежные транзакции"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['type', '-date']),
        ]
    
    def __str__(self):
        type_display = self.get_type_display()
        return f"{type_display}: {self.amount} ₽ ({self.date.strftime('%d.%m.%Y')})"


class ProfitReport(models.Model):
    """Модель отчёта о прибыли (кэш для быстрого доступа)"""
    
    date = models.DateField(
        unique=True,
        verbose_name="Дата"
    )
    
    # Выручка
    revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Выручка"
    )
    
    # Себестоимость проданных товаров
    cost_of_goods = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Себестоимость товаров"
    )
    
    # Валовая прибыль (revenue - cost_of_goods)
    gross_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Валовая прибыль"
    )
    
    # Операционные расходы
    operating_expenses = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Операционные расходы"
    )
    
    # Чистая прибыль (gross_profit - operating_expenses)
    net_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Чистая прибыль"
    )
    
    # Количество заказов
    orders_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество заказов"
    )
    
    # Средний чек
    average_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Средний чек"
    )
    
    # Маржа (%)
    margin_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Маржа (%)"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено"
    )
    
    class Meta:
        verbose_name = "Отчёт о прибыли"
        verbose_name_plural = "Отчёты о прибыли"
        ordering = ['-date']
    
    def __str__(self):
        return f"Отчёт {self.date}: прибыль {self.net_profit} ₽"

