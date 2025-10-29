from django.contrib import admin
from django.utils.html import format_html
from .models import SeoPage, SeoSettings


@admin.register(SeoPage)
class SeoPageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['slug', 'title', 'description']
    ordering = ['slug']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('slug', 'is_active')
        }),
        ('SEO метатеги', {
            'fields': ('title', 'description', 'keywords', 'canonical_url', 'robots')
        }),
        ('Open Graph', {
            'fields': ('og_title', 'og_description', 'og_image', 'og_image_url'),
            'classes': ('collapse',)
        }),
        ('Подтверждения', {
            'fields': ('yandex_verification',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset().select_related()


@admin.register(SeoSettings)
class SeoSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'yandex_verification', 'google_verification', 'updated_at']
    
    fieldsets = (
        ('Основные настройки', {
            'fields': ('site_name', 'site_description', 'default_og_image')
        }),
        ('Подтверждения поисковых систем', {
            'fields': ('yandex_verification', 'google_verification'),
            'classes': ('collapse',)
        }),
        ('Аналитика', {
            'fields': ('yandex_metrica', 'google_analytics'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Разрешаем добавление только если нет записей
        return not SeoSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление настроек
        return False








