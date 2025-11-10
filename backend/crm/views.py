from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Customer, CustomerNote
from .serializers import CustomerSerializer, CustomerNoteSerializer
from orders.serializers import OrderListSerializer


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
        
        # Получаем уникальных клиентов из заказов
        orders = Order.objects.values('customer_name', 'customer_phone', 'customer_email', 'delivery_city').distinct()
        
        created_count = 0
        for order_data in orders:
            if not order_data['customer_phone']:
                continue
            
            customer, created = Customer.objects.get_or_create(
                phone=order_data['customer_phone'],
                defaults={
                    'name': order_data['customer_name'] or 'Без имени',
                    'email': order_data['customer_email'] or '',
                    'city': order_data['delivery_city'] or ''
                }
            )
            
            if created:
                created_count += 1
            
            # Обновляем статистику
            customer.update_statistics()
        
        return Response({
            'status': 'success',
            'created_count': created_count,
            'total_customers': Customer.objects.count()
        })


class CustomerNoteViewSet(viewsets.ModelViewSet):
    """ViewSet для заметок о клиентах"""
    
    queryset = CustomerNote.objects.select_related('customer', 'created_by').all()
    serializer_class = CustomerNoteSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer']

