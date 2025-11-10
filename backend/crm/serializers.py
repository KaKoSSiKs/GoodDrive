from rest_framework import serializers
from .models import Customer, CustomerNote


class CustomerSerializer(serializers.ModelSerializer):
    """Сериализатор клиента"""
    
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    lifetime_value = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'phone', 'email', 'city', 'address',
            'category', 'category_display',
            'total_orders', 'total_spent', 'average_order',
            'last_order_date', 'lifetime_value',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_orders', 'total_spent', 'average_order', 'last_order_date', 'created_at', 'updated_at']
    
    def get_lifetime_value(self, obj):
        return obj.get_lifetime_value()


class CustomerNoteSerializer(serializers.ModelSerializer):
    """Сериализатор заметки о клиенте"""
    
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = CustomerNote
        fields = ['id', 'customer', 'note', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

