import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    """Фильтры для модели Order"""
    
    # Фильтрация по статусу
    status = django_filters.ChoiceFilter(
        choices=Order.STATUS_CHOICES,
        field_name='status'
    )
    
    # Фильтрация по диапазону сумм
    total_amount_min = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='gte'
    )
    total_amount_max = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='lte'
    )
    
    # Фильтрация по дате создания
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    # Фильтрация по городу доставки
    delivery_city = django_filters.CharFilter(
        field_name='delivery_city',
        lookup_expr='icontains'
    )
    
    # Фильтрация по наличию email
    has_email = django_filters.BooleanFilter(
        method='filter_has_email'
    )
    
    # Фильтрация по наличию комментариев
    has_notes = django_filters.BooleanFilter(
        method='filter_has_notes'
    )
    
    class Meta:
        model = Order
        fields = [
            'status', 'total_amount_min', 'total_amount_max',
            'created_after', 'created_before', 'delivery_city',
            'has_email', 'has_notes'
        ]
    
    def filter_has_email(self, queryset, name, value):
        """Фильтр по наличию email"""
        if value:
            return queryset.exclude(customer_email__isnull=True).exclude(customer_email='')
        else:
            return queryset.filter(customer_email__isnull=True) | queryset.filter(customer_email='')
    
    def filter_has_notes(self, queryset, name, value):
        """Фильтр по наличию комментариев"""
        if value:
            return queryset.exclude(notes__isnull=True).exclude(notes='')
        else:
            return queryset.filter(notes__isnull=True) | queryset.filter(notes='')








