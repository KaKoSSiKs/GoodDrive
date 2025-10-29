from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['part', 'quantity', 'unit_price', 'total_price']


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['created_at', 'created_by']
    fields = ['status', 'comment', 'created_at', 'created_by']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer_name', 'customer_phone', 
        'total_amount', 'status', 'delivery_city', 'created_at'
    ]
    list_filter = [
        'status', 'delivery_city', 'created_at', 'updated_at'
    ]
    search_fields = [
        'order_number', 'customer_name', 'customer_phone', 
        'customer_email', 'delivery_address'
    ]
    readonly_fields = [
        'order_number', 'total_amount', 'created_at', 'updated_at'
    ]
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('order_number', 'status', 'total_amount')
        }),
        ('Контактная информация', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Адрес доставки', {
            'fields': ('delivery_address', 'delivery_city', 'delivery_postal_code')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset().select_related().prefetch_related('items__part')
    
    def save_model(self, request, obj, form, change):
        """Сохранение модели с записью в историю"""
        old_status = None
        if change:
            old_status = Order.objects.get(pk=obj.pk).status
        
        super().save_model(request, obj, form, change)
        
        # Если статус изменился, записываем в историю
        if change and old_status != obj.status:
            OrderStatusHistory.objects.create(
                order=obj,
                status=obj.status,
                comment=f"Статус изменен администратором",
                created_by=request.user
            )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'part', 'quantity', 'unit_price', 
        'total_price', 'get_order_status'
    ]
    list_filter = ['order__status', 'order__created_at']
    search_fields = [
        'order__order_number', 'part__title', 
        'part__original_number', 'part__manufacturer_number'
    ]
    readonly_fields = ['total_price']
    
    def get_order_status(self, obj):
        """Получить статус заказа"""
        return obj.order.get_status_display()
    get_order_status.short_description = 'Статус заказа'
    
    def get_queryset(self, request):
        return super().get_queryset().select_related('order', 'part')


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'status', 'comment', 'created_at', 'created_by'
    ]
    list_filter = ['status', 'created_at']
    search_fields = [
        'order__order_number', 'comment'
    ]
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset().select_related('order', 'created_by')








