from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import logging
from .models import ExpenseCategory, Expense, CashTransaction, ProfitReport
from .serializers import (
    ExpenseCategorySerializer,
    ExpenseSerializer,
    CashTransactionSerializer,
    ProfitReportSerializer
)

logger = logging.getLogger(__name__)


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
    
    def destroy(self, request, *args, **kwargs):
        """Удаление расхода с логированием"""
        expense = self.get_object()
        
        try:
            with transaction.atomic():
                # Логируем удаление
                logger.warning(
                    f"Удаление расхода ID:{expense.id} | "
                    f"Категория: {expense.category.name if expense.category else 'Без категории'} | "
                    f"Сумма: {expense.amount} ₽ | "
                    f"Дата: {expense.date} | "
                    f"Описание: {expense.description[:50]} | "
                    f"Пользователь: {request.user.username if request.user.is_authenticated else 'Неизвестен'}"
                )
                
                deleted_data = {
                    'id': expense.id,
                    'category': expense.category.name if expense.category else None,
                    'amount': str(expense.amount),
                    'date': str(expense.date),
                    'description': expense.description
                }
                
                expense.delete()
                
                return Response({
                    'status': 'success',
                    'message': 'Расход успешно удален',
                    'deleted_expense': deleted_data
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"Ошибка при удалении расхода ID:{expense.id}: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Ошибка при удалении расхода: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    
    def destroy(self, request, *args, **kwargs):
        """Удаление транзакции с логированием и пересчетом баланса"""
        transaction_obj = self.get_object()
        
        # Проверка связи с заказом
        if transaction_obj.order:
            logger.warning(
                f"Попытка удаления транзакции ID:{transaction_obj.id}, связанной с заказом #{transaction_obj.order.order_number}"
            )
            return Response({
                'status': 'error',
                'message': f'Эта транзакция связана с заказом #{transaction_obj.order.order_number}. Удалите заказ или отвяжите транзакцию.',
                'order_number': transaction_obj.order.order_number
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                # Логируем удаление
                logger.warning(
                    f"Удаление транзакции ID:{transaction_obj.id} | "
                    f"Тип: {transaction_obj.get_type_display()} | "
                    f"Сумма: {transaction_obj.amount} ₽ | "
                    f"Способ: {transaction_obj.get_payment_method_display()} | "
                    f"Дата: {transaction_obj.date} | "
                    f"Описание: {transaction_obj.description[:50] if transaction_obj.description else 'Нет'} | "
                    f"Пользователь: {request.user.username if request.user.is_authenticated else 'Неизвестен'}"
                )
                
                deleted_data = {
                    'id': transaction_obj.id,
                    'type': transaction_obj.type,
                    'type_display': transaction_obj.get_type_display(),
                    'amount': str(transaction_obj.amount),
                    'payment_method': transaction_obj.payment_method,
                    'date': str(transaction_obj.date),
                    'description': transaction_obj.description
                }
                
                transaction_obj.delete()
                
                # Пересчитываем баланс
                income = CashTransaction.objects.filter(type='income').aggregate(
                    total=Sum('amount')
                )['total'] or 0
                
                expense = CashTransaction.objects.filter(type='expense').aggregate(
                    total=Sum('amount')
                )['total'] or 0
                
                new_balance = income - expense
                
                return Response({
                    'status': 'success',
                    'message': 'Транзакция успешно удалена',
                    'deleted_transaction': deleted_data,
                    'current_balance': {
                        'income': str(income),
                        'expense': str(expense),
                        'balance': str(new_balance)
                    }
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"Ошибка при удалении транзакции ID:{transaction_obj.id}: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Ошибка при удалении транзакции: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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

