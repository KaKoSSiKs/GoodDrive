from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Brand, Warehouse, Part, PartImage
from .serializers import (
    BrandSerializer, WarehouseSerializer, 
    PartListSerializer, PartDetailSerializer, PartCreateUpdateSerializer
)
from .filters import PartFilter


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для брендов (только чтение)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'country']
    ordering = ['name']


class WarehouseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для складов (только чтение)"""
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name']
    ordering = ['name']


class PartViewSet(viewsets.ModelViewSet):
    """ViewSet для автозапчастей"""
    queryset = Part.objects.select_related('brand', 'warehouse').prefetch_related('images')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PartFilter
    search_fields = ['title', 'label', 'original_number', 'manufacturer_number', 'description']
    ordering_fields = ['title', 'price_opt', 'available', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""
        if self.action == 'list':
            return PartListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PartCreateUpdateSerializer
        return PartDetailSerializer
    
    def get_queryset(self):
        """Фильтруем только активные автозапчасти по умолчанию"""
        queryset = super().get_queryset()
        
        # Если не указан параметр show_inactive, показываем только активные
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        if not show_inactive:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Получить только доступные автозапчасти (available > 0)"""
        queryset = self.get_queryset().filter(available__gt=0)
        
        # Применяем фильтры
        queryset = self.filter_queryset(queryset)
        
        # Пагинация
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PartListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PartListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Получить автозапчасти с низким остатком (available <= 5)"""
        queryset = self.get_queryset().filter(available__lte=5)
        
        # Применяем фильтры
        queryset = self.filter_queryset(queryset)
        
        # Пагинация
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PartListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PartListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """Получить похожие автозапчасти (того же бренда)"""
        part = self.get_object()
        similar_parts = self.get_queryset().filter(
            brand=part.brand,
            is_active=True
        ).exclude(id=part.id)[:5]
        
        serializer = PartListSerializer(similar_parts, many=True)
        return Response(serializer.data)

