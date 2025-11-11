from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
import logging
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer,
    OrderListSerializer, OrderStatusHistorySerializer
)
from .filters import OrderFilter

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заказами"""
    queryset = Order.objects.select_related().prefetch_related('items__part', 'status_history').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ['order_number', 'customer_name', 'customer_phone', 'customer_email']
    ordering_fields = ['created_at', 'total_amount', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        elif self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    def get_permissions(self):
        """Права доступа в зависимости от действия"""
        if self.action in ['create', 'statistics', 'list', 'retrieve', 'update_status', 'status_history']:
            # Создание заказа, просмотр и изменение статуса доступно всем (для админки)
            permission_classes = [AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update']:
            # Удаление и изменение заказа только для авторизованных
            permission_classes = [IsAuthenticated]
        else:
            # Остальные действия только для авторизованных
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Создание нового заказа"""
        logger.info(f"Order creation request data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Order validation errors: {serializer.errors}")
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Отправляем уведомление о новом заказе
        try:
            from notifications.utils import notify_new_order
            notify_new_order(order)
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
        
        # Возвращаем полную информацию о заказе
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """Удаление заказа с логированием и обновлением статистики CRM"""
        order = self.get_object()
        order_number = order.order_number
        customer_phone = order.customer_phone
        items_count = order.items.count()
        total_amount = order.total_amount
        
        try:
            with transaction.atomic():
                # Логируем удаление
                logger.warning(
                    f"Удаление заказа #{order_number} | "
                    f"Клиент: {customer_phone} | "
                    f"Позиций: {items_count} | "
                    f"Сумма: {total_amount} ₽ | "
                    f"Пользователь: {request.user.username if request.user.is_authenticated else 'Неизвестен'}"
                )
                
                # Удаляем заказ (связанные объекты удалятся автоматически через CASCADE)
                order.delete()
                
                # Обновляем статистику клиента в CRM
                try:
                    from crm.models import Customer
                    customer = Customer.objects.filter(phone=customer_phone).first()
                    if customer:
                        customer.update_statistics()
                        logger.info(f"Статистика CRM обновлена для клиента {customer_phone}")
                except Exception as e:
                    logger.error(f"Ошибка обновления CRM после удаления заказа: {e}")
                
                return Response({
                    'status': 'success',
                    'message': f'Заказ #{order_number} успешно удален',
                    'deleted_order': {
                        'order_number': order_number,
                        'customer_phone': customer_phone,
                        'items_count': items_count,
                        'total_amount': str(total_amount)
                    }
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"Ошибка при удалении заказа #{order_number}: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Ошибка при удалении заказа: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def status_history(self, request, pk=None):
        """Получить историю статусов заказа"""
        order = self.get_object()
        history = order.status_history.all()
        serializer = OrderStatusHistorySerializer(history, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def update_status(self, request, pk=None):
        """Обновить статус заказа"""
        order = self.get_object()
        new_status = request.data.get('status')
        comment = request.data.get('comment', '')
        
        if not new_status:
            return Response(
                {'error': 'Статус не указан'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем валидность статуса
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Недопустимый статус. Доступные: {valid_statuses}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = order.status
        order.status = new_status
        order.save()
        
        # Записываем в историю
        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            comment=comment,
            created_by=request.user if request.user.is_authenticated else None
        )
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_phone(self, request):
        """Получить заказы по номеру телефона"""
        phone = request.query_params.get('phone')
        if not phone:
            return Response(
                {'error': 'Номер телефона не указан'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orders = self.get_queryset().filter(customer_phone=phone)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def statistics(self, request):
        """Получить статистику заказов"""
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        # Общая статистика
        total_orders = Order.objects.count()
        total_amount = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Статистика по статусам
        status_stats = Order.objects.values('status').annotate(count=Count('id'))
        
        # Статистика за последние 30 дней
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago)
        recent_count = recent_orders.count()
        recent_amount = recent_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Средний чек
        avg_order_amount = Order.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0
        
        return Response({
            'total_orders': total_orders,
            'total_amount': float(total_amount),
            'avg_order_amount': float(avg_order_amount),
            'status_statistics': list(status_stats),
            'recent_30_days': {
                'orders_count': recent_count,
                'total_amount': float(recent_amount)
            }
        })


class OrderStatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для истории статусов заказов (только чтение)"""
    queryset = OrderStatusHistory.objects.select_related('order', 'created_by').all()
    serializer_class = OrderStatusHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Фильтрация по заказу"""
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset








