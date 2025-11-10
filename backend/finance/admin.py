from django.contrib import admin
from .models import ExpenseCategory, Expense, CashTransaction, ProfitReport


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'date', 'created_by', 'created_at']
    list_filter = ['category', 'date']
    search_fields = ['description']
    ordering = ['-date']


@admin.register(CashTransaction)
class CashTransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'amount', 'payment_method', 'date', 'order', 'created_by']
    list_filter = ['type', 'payment_method', 'date']
    search_fields = ['description']
    ordering = ['-date']


@admin.register(ProfitReport)
class ProfitReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'revenue', 'net_profit', 'margin_percent', 'orders_count']
    list_filter = ['date']
    ordering = ['-date']

