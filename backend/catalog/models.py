from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import os


def part_image_upload_path(instance, filename):
    """Генерирует путь для загрузки изображений автозапчастей"""
    return f'parts/{instance.part.id}/{filename}'


class Brand(models.Model):
    """Модель бренда автозапчастей"""
    name = models.CharField(max_length=100, verbose_name="Название бренда")
    country = models.CharField(max_length=50, verbose_name="Страна")
    site = models.URLField(blank=True, null=True, verbose_name="Официальный сайт")
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Warehouse(models.Model):
    """Модель склада"""
    name = models.CharField(max_length=200, verbose_name="Название склада")
    address = models.TextField(verbose_name="Адрес склада")
    
    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Part(models.Model):
    """Модель автозапчасти"""
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    title = models.CharField(max_length=200, verbose_name="Название")
    label = models.CharField(max_length=100, blank=True, verbose_name="Метка")
    original_number = models.CharField(max_length=50, blank=True, verbose_name="Оригинальный номер")
    manufacturer_number = models.CharField(max_length=50, blank=True, verbose_name="Номер производителя")
    
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.CASCADE, 
        related_name='parts',
        verbose_name="Бренд"
    )
    warehouse = models.ForeignKey(
        Warehouse, 
        on_delete=models.CASCADE, 
        related_name='parts',
        verbose_name="Склад"
    )
    
    quantity = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="Общее количество"
    )
    stock = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="На складе"
    )
    reserve = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="В резерве"
    )
    available = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="Доступно"
    )
    
    price_opt = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Оптовая цена"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Автозапчасть"
        verbose_name_plural = "Автозапчасти"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['brand', 'is_active']),
            models.Index(fields=['warehouse', 'is_active']),
            models.Index(fields=['price_opt']),
            models.Index(fields=['available']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.brand.name})"
    
    def save(self, *args, **kwargs):
        # Автоматически вычисляем доступное количество
        self.available = max(0, self.stock - self.reserve)
        super().save(*args, **kwargs)


class PartImage(models.Model):
    """Модель изображения автозапчасти"""
    part = models.ForeignKey(
        Part, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Автозапчасть"
    )
    image = models.ImageField(
        upload_to=part_image_upload_path,
        verbose_name="Изображение"
    )
    image_url = models.URLField(blank=True, null=True, verbose_name="URL изображения")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст")
    order_index = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    
    class Meta:
        verbose_name = "Изображение автозапчасти"
        verbose_name_plural = "Изображения автозапчастей"
        ordering = ['order_index', 'id']
    
    def __str__(self):
        return f"Изображение {self.part.title}"
    
    def save(self, *args, **kwargs):
        # Если загружено локальное изображение, генерируем URL
        if self.image and not self.image_url:
            self.image_url = self.image.url
        super().save(*args, **kwargs)
    
    @property
    def get_image_url(self):
        """Возвращает URL изображения (локальное или внешнее)"""
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return None
