from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import ExpenseCategory, Expense, CashTransaction, ProfitReport
from .serializers import (
    ExpenseCategorySerializer,
    ExpenseSerializer,
    CashTransactionSerializer,
    ProfitReportSerializer
)


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий расходов"""
    
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [AllowAny]


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet для расходов"""
    
    queryset = Expense.objects.select_related('category', 'created_by').all()
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'date']
    search_fields = ['description']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']


class CashTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet для денежных транзакций"""
    
    queryset = CashTransaction.objects.select_related('order', 'expense', 'created_by').all()
    serializer_class = CashTransactionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'payment_method', 'date']
    search_fields = ['description']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'])
    def balance(self, request):
        """Получить текущий баланс кассы"""
        income = CashTransaction.objects.filter(type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense = CashTransaction.objects.filter(type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        balance = income - expense
        
        return Response({
            'income': income,
            'expense': expense,
            'balance': balance
        })


class ProfitReportViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для отчётов о прибыли"""
    
    queryset = ProfitReport.objects.all()
    serializer_class = ProfitReportSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Получить сводку по прибыли за период"""
        from orders.models import Order
        from orders.serializers import OrderSerializer
        
        # Параметры периода
        period = request.query_params.get('period', '30')  # дней
        days_ago = int(period)
        date_from = timezone.now() - timedelta(days=days_ago)
        
        # Заказы за период
        orders = Order.objects.filter(
            created_at__gte=date_from,
            status='completed'
        ).select_related().prefetch_related('items__part')
        
        # Подсчёт метрик
        total_revenue = 0
        total_cost = 0
        
        for order in orders:
            for item in order.items.all():
                total_revenue += float(item.unit_price) * item.quantity
                # Себестоимость товара
                if hasattr(item.part, 'cost_price'):
                    total_cost += float(item.part.cost_price) * item.quantity
        
        # Расходы за период
        expenses = Expense.objects.filter(date__gte=date_from).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Расчёт прибыли
        gross_profit = total_revenue - total_cost
        net_profit = gross_profit - float(expenses)
        
        # Маржа
        margin_percent = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Средний чек
        orders_count = orders.count()
        average_order = total_revenue / orders_count if orders_count > 0 else 0
        
        return Response({
            'period_days': days_ago,
            'date_from': date_from.date(),
            'revenue': round(total_revenue, 2),
            'cost_of_goods': round(total_cost, 2),
            'gross_profit': round(gross_profit, 2),
            'operating_expenses': round(float(expenses), 2),
            'net_profit': round(net_profit, 2),
            'orders_count': orders_count,
            'average_order': round(average_order, 2),
            'margin_percent': round(margin_percent, 2)
        })

