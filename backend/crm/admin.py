from django.contrib import admin
from .models import Customer, CustomerNote


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'category', 'total_orders', 'total_spent', 'last_order_date']
    list_filter = ['category', 'city']
    search_fields = ['name', 'phone', 'email']
    ordering = ['-total_spent']


@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['note', 'customer__name']

