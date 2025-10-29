from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderStatusHistoryViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-status-history', OrderStatusHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]








