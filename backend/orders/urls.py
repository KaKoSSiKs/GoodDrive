from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderStatusHistoryViewSet
from .print_views import print_invoice, print_receipt, export_to_1c

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-status-history', OrderStatusHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/<int:order_id>/print-invoice/', print_invoice, name='print-invoice'),
    path('orders/<int:order_id>/print-receipt/', print_receipt, name='print-receipt'),
    path('orders/export-1c/', export_to_1c, name='export-1c'),
]








