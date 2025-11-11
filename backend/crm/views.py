from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
import logging
from .models import Customer, CustomerNote
from .serializers import CustomerSerializer, CustomerNoteSerializer
from orders.serializers import OrderListSerializer

logger = logging.getLogger(__name__)


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet для клиентов"""
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['created_at', 'total_spent', 'total_orders', 'last_order_date']
    ordering = ['-total_spent']
    
    @action(detail=True, methods=['get'])
    def orders_history(self, request, pk=None):
        """Получить историю заказов клиента"""
        customer = self.get_object()
        orders = customer.get_orders_history()
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_stats(self, request, pk=None):
        """Обновить статистику клиента"""
        customer = self.get_object()
        customer.update_statistics()
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def sync_from_orders(self, request):
        """Синхронизировать клиентов из заказов"""
        from orders.models import Order
        
        try:
            # Получаем уникальные телефоны из заказов
            unique_phones = Order.objects.exclude(
                customer_phone__isnull=True
            ).exclude(
                customer_phone=''
            ).values_list('customer_phone', flat=True).distinct()
            
            created_count = 0
            updated_count = 0
            error_count = 0
            errors = []
            
            for phone in unique_phones:
                try:
                    # Получаем последний заказ клиента для актуальных данных
                    latest_order = Order.objects.filter(
                        customer_phone=phone
                    ).order_by('-created_at').first()
                    
                    if not latest_order:
                        continue
                    
                    with transaction.atomic():
                        # Создаем или обновляем клиента
                        customer, created = Customer.objects.get_or_create(
                            phone=phone,
                            defaults={
                                'name': latest_order.customer_name or 'Без имени',
                                'email': latest_order.customer_email or '',
                                'city': latest_order.delivery_city or ''
                            }
                        )
                        
                        if created:
                            created_count += 1
                            logger.info(f"Создан новый клиент: {phone}")
                        else:
                            # Обновляем данные существующего клиента из последнего заказа
                            updated = False
                            if latest_order.customer_name and customer.name != latest_order.customer_name:
                                customer.name = latest_order.customer_name
                                updated = True
                            if latest_order.customer_email and customer.email != latest_order.customer_email:
                                customer.email = latest_order.customer_email
                                updated = True
                            if latest_order.delivery_city and customer.city != latest_order.delivery_city:
                                customer.city = latest_order.delivery_city
                                updated = True
                            
                            if updated:
                                customer.save()
                                updated_count += 1
                                logger.info(f"Обновлен клиент: {phone}")
                        
                        # Обновляем статистику клиента
                        customer.update_statistics()
                        
                except Exception as e:
                    error_count += 1
                    error_msg = f"Ошибка синхронизации клиента {phone}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    continue
            
            response_data = {
                'status': 'success' if error_count == 0 else 'partial_success',
                'created_count': created_count,
                'updated_count': updated_count,
                'error_count': error_count,
                'total_customers': Customer.objects.count()
            }
            
            if errors:
                response_data['errors'] = errors[:10]  # Возвращаем первые 10 ошибок
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Критическая ошибка синхронизации CRM: {str(e)}")
            return Response({
                'status': 'error',
                'message': f"Ошибка синхронизации: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerNoteViewSet(viewsets.ModelViewSet):
    """ViewSet для заметок о клиентах"""
    
    queryset = CustomerNote.objects.select_related('customer', 'created_by').all()
    serializer_class = CustomerNoteSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer']

