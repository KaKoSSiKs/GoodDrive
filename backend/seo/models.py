from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator


class SeoPage(models.Model):
    """Модель для SEO метаданных страниц"""
    slug = models.SlugField(
        unique=True, 
        verbose_name="URL страницы",
        help_text="Уникальный идентификатор страницы (например: 'home', 'catalog', 'about')"
    )
    title = models.CharField(
        max_length=60, 
        verbose_name="Title",
        help_text="Заголовок страницы (до 60 символов)"
    )
    description = models.TextField(
        max_length=160,
        validators=[MaxLengthValidator(160)],
        verbose_name="Description",
        help_text="Описание страницы (до 160 символов)"
    )
    keywords = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="Keywords",
        help_text="Ключевые слова через запятую"
    )
    
    # Open Graph метатеги
    og_title = models.CharField(
        max_length=60, 
        blank=True,
        verbose_name="OG Title",
        help_text="Заголовок для социальных сетей"
    )
    og_description = models.TextField(
        max_length=160,
        validators=[MaxLengthValidator(160)],
        blank=True,
        verbose_name="OG Description",
        help_text="Описание для социальных сетей"
    )
    og_image = models.ImageField(
        upload_to='seo/og_images/',
        blank=True,
        null=True,
        verbose_name="OG Image",
        help_text="Изображение для социальных сетей (1200x630px)"
    )
    og_image_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="OG Image URL",
        help_text="Внешний URL изображения для социальных сетей"
    )
    
    # Дополнительные метатеги
    canonical_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Canonical URL",
        help_text="Канонический URL страницы"
    )
    robots = models.CharField(
        max_length=100,
        default="index, follow",
        verbose_name="Robots",
        help_text="Директивы для поисковых роботов"
    )
    
    # Яндекс.Вебмастер
    yandex_verification = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Yandex Verification",
        help_text="Код подтверждения Яндекс.Вебмастер"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "SEO страница"
        verbose_name_plural = "SEO страницы"
        ordering = ['slug']
    
    def __str__(self):
        return f"{self.slug} - {self.title}"
    
    @property
    def get_og_image_url(self):
        """Возвращает URL изображения для Open Graph"""
        if self.og_image_url:
            return self.og_image_url
        elif self.og_image:
            return self.og_image.url
        return None


class SeoSettings(models.Model):
    """Глобальные SEO настройки сайта"""
    site_name = models.CharField(
        max_length=100,
        default="GoodDrive",
        verbose_name="Название сайта"
    )
    site_description = models.TextField(
        max_length=160,
        validators=[MaxLengthValidator(160)],
        default="Интернет-магазин автозапчастей GoodDrive",
        verbose_name="Описание сайта"
    )
    default_og_image = models.ImageField(
        upload_to='seo/default/',
        blank=True,
        null=True,
        verbose_name="Изображение по умолчанию для OG",
        help_text="Изображение по умолчанию для социальных сетей"
    )
    
    # Яндекс.Вебмастер
    yandex_verification = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Yandex Verification",
        help_text="Код подтверждения Яндекс.Вебмастер"
    )
    
    # Google Search Console
    google_verification = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Google Verification",
        help_text="Код подтверждения Google Search Console"
    )
    
    # Яндекс.Метрика
    yandex_metrica = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Yandex Metrica ID",
        help_text="ID счетчика Яндекс.Метрики"
    )
    
    # Google Analytics
    google_analytics = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Google Analytics ID",
        help_text="ID счетчика Google Analytics"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "SEO настройки"
        verbose_name_plural = "SEO настройки"
    
    def __str__(self):
        return f"SEO настройки - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Обеспечиваем единственную запись настроек
        if not self.pk and SeoSettings.objects.exists():
            return
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Получает единственную запись настроек или создает новую"""
        settings, created = cls.objects.get_or_create(
            defaults={
                'site_name': 'GoodDrive',
                'site_description': 'Интернет-магазин автозапчастей GoodDrive'
            }
        )
        return settings








