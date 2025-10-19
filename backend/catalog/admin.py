from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Warehouse, Part, PartImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'site', 'parts_count']
    list_filter = ['country']
    search_fields = ['name', 'country']
    ordering = ['name']
    
    def parts_count(self, obj):
        return obj.parts.filter(is_active=True).count()
    parts_count.short_description = 'Количество активных запчастей'


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'parts_count']
    search_fields = ['name', 'address']
    ordering = ['name']
    
    def parts_count(self, obj):
        return obj.parts.filter(is_active=True).count()
    parts_count.short_description = 'Количество активных запчастей'


class PartImageInline(admin.TabularInline):
    model = PartImage
    extra = 1
    fields = ['image', 'image_url', 'alt_text', 'order_index']
    readonly_fields = ['image_url']


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'brand', 'warehouse', 'price_opt', 
        'available', 'is_active', 'created_at'
    ]
    list_filter = [
        'is_active', 'brand', 'warehouse', 'created_at'
    ]
    search_fields = [
        'title', 'label', 'original_number', 
        'manufacturer_number', 'description'
    ]
    ordering = ['-created_at']
    inlines = [PartImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('is_active', 'title', 'label', 'description')
        }),
        ('Номера', {
            'fields': ('original_number', 'manufacturer_number')
        }),
        ('Связи', {
            'fields': ('brand', 'warehouse')
        }),
        ('Количество и цены', {
            'fields': ('quantity', 'stock', 'reserve', 'available', 'price_opt')
        }),
    )
    
    readonly_fields = ['available']
    
    def get_queryset(self, request):
        return super().get_queryset().select_related('brand', 'warehouse')


@admin.register(PartImage)
class PartImageAdmin(admin.ModelAdmin):
    list_display = ['part', 'get_image_preview', 'alt_text', 'order_index']
    list_filter = ['part__brand', 'part__warehouse']
    search_fields = ['part__title', 'alt_text']
    ordering = ['part', 'order_index']
    
    def get_queryset(self, request):
        return super().get_queryset().select_related('part__brand', 'part__warehouse')
    
    def get_image_preview(self, obj):
        """Показывает превью изображения в админке"""
        if obj.get_image_url:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.get_image_url
            )
        return "Нет изображения"
    get_image_preview.short_description = 'Превью'
