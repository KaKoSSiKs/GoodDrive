import django_filters
from django.db.models import Q
from .models import Part, Brand, Warehouse


class PartFilter(django_filters.FilterSet):
    """Фильтр для автозапчастей"""
    
    # Фильтр по бренду
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all())
    brand_name = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    
    # Фильтр по складу
    warehouse = django_filters.ModelChoiceFilter(queryset=Warehouse.objects.all())
    warehouse_name = django_filters.CharFilter(field_name='warehouse__name', lookup_expr='icontains')
    
    # Фильтр по цене
    price_min = django_filters.NumberFilter(field_name='price_opt', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price_opt', lookup_expr='lte')
    
    # Фильтр по наличию
    available_min = django_filters.NumberFilter(field_name='available', lookup_expr='gte')
    available_max = django_filters.NumberFilter(field_name='available', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(field_name='available', lookup_expr='gt', method='filter_in_stock')
    
    # Фильтр по активности
    is_active = django_filters.BooleanFilter(field_name='is_active')
    
    # Фильтр по номерам
    original_number = django_filters.CharFilter(field_name='original_number', lookup_expr='icontains')
    manufacturer_number = django_filters.CharFilter(field_name='manufacturer_number', lookup_expr='icontains')
    
    # Фильтр по дате создания
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    # Комбинированный поиск
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Part
        fields = [
            'brand', 'brand_name', 'warehouse', 'warehouse_name',
            'price_min', 'price_max', 'available_min', 'available_max',
            'in_stock', 'is_active', 'original_number', 'manufacturer_number',
            'created_after', 'created_before', 'search'
        ]
    
    def filter_in_stock(self, queryset, name, value):
        """Фильтр по наличию на складе"""
        if value:
            return queryset.filter(available__gt=0)
        return queryset.filter(available=0)
    
    def filter_search(self, queryset, name, value):
        """Комбинированный поиск по нескольким полям"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(label__icontains=value) |
            Q(original_number__icontains=value) |
            Q(manufacturer_number__icontains=value) |
            Q(description__icontains=value) |
            Q(brand__name__icontains=value)
        )

