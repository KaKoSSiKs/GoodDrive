from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """Модель уведомлений"""
    
    TYPE_CHOICES = [
        ('new_order', 'Новый заказ'),
        ('low_stock', 'Низкий остаток'),
        ('zero_stock', 'Нулевой остаток'),
        ('stuck_order', 'Заказ застрял'),
        ('system', 'Системное'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический'),
    ]
    
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Тип уведомления"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Приоритет"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    message = models.TextField(
        verbose_name="Сообщение"
    )
    link = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Прочитано"
    )
    is_sent_email = models.BooleanField(
        default=False,
        verbose_name="Email отправлен"
    )
    related_order_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID связанного заказа"
    )
    related_part_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID связанного товара"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_read', '-created_at']),
            models.Index(fields=['type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"


class NotificationSettings(models.Model):
    """Настройки уведомлений"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_settings',
        verbose_name="Пользователь"
    )
    
    # Email уведомления
    email_new_order = models.BooleanField(
        default=True,
        verbose_name="Email при новом заказе"
    )
    email_low_stock = models.BooleanField(
        default=True,
        verbose_name="Email при низком остатке"
    )
    
    # Push уведомления
    push_new_order = models.BooleanField(
        default=True,
        verbose_name="Push при новом заказе"
    )
    push_low_stock = models.BooleanField(
        default=False,
        verbose_name="Push при низком остатке"
    )
    
    # Звуковые уведомления
    sound_enabled = models.BooleanField(
        default=True,
        verbose_name="Звуковые уведомления"
    )
    
    # Email для уведомлений
    notification_email = models.EmailField(
        blank=True,
        verbose_name="Email для уведомлений"
    )
    
    class Meta:
        verbose_name = "Настройки уведомлений"
        verbose_name_plural = "Настройки уведомлений"
    
    def __str__(self):
        return f"Настройки {self.user.username}"

