from rest_framework import serializers
from .models import ExpenseCategory, Expense, CashTransaction, ProfitReport


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории расходов"""
    
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'description', 'is_active']


class ExpenseSerializer(serializers.ModelSerializer):
    """Сериализатор расхода"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id',
            'category',
            'category_name',
            'amount',
            'description',
            'date',
            'created_by',
            'created_by_name',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class CashTransactionSerializer(serializers.ModelSerializer):
    """Сериализатор денежной транзакции"""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = CashTransaction
        fields = [
            'id',
            'type',
            'type_display',
            'amount',
            'payment_method',
            'payment_method_display',
            'description',
            'order',
            'order_number',
            'expense',
            'date',
            'created_by',
            'created_by_name',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class ProfitReportSerializer(serializers.ModelSerializer):
    """Сериализатор отчёта о прибыли"""
    
    class Meta:
        model = ProfitReport
        fields = [
            'id',
            'date',
            'revenue',
            'cost_of_goods',
            'gross_profit',
            'operating_expenses',
            'net_profit',
            'orders_count',
            'average_order',
            'margin_percent',
            'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']

