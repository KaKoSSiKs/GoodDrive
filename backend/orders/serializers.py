from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from catalog.serializers import PartListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции заказа"""
    part = PartListSerializer(read_only=True)
    part_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'part', 'part_id', 'quantity', 
            'unit_price', 'total_price'
        ]
        read_only_fields = ['id', 'total_price']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для истории статусов заказа"""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'status', 'comment', 'created_at', 
            'created_by_name'
        ]
        read_only_fields = ['id', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказа"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone', 
            'customer_email', 'delivery_address', 'delivery_city', 
            'delivery_postal_code', 'total_amount', 'status', 
            'status_display', 'notes', 'created_at', 'updated_at',
            'items', 'status_history'
        ]
        read_only_fields = [
            'id', 'order_number', 'total_amount', 'created_at', 
            'updated_at', 'status_history'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа"""
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_phone', 'customer_email',
            'delivery_address', 'delivery_city', 'delivery_postal_code',
            'notes', 'items'
        ]
    
    def validate_items(self, value):
        """Валидация позиций заказа"""
        if not value:
            raise serializers.ValidationError("Заказ должен содержать хотя бы одну позицию")
        
        for item in value:
            # Проверяем доступность товара
            part_id = item['part_id']
            quantity = item['quantity']
            
            try:
                from catalog.models import Part
                part = Part.objects.get(id=part_id)
                if part.available < quantity:
                    raise serializers.ValidationError(
                        f"Недостаточно товара '{part.title}'. Доступно: {part.available}"
                    )
            except Part.DoesNotExist:
                raise serializers.ValidationError(f"Товар с ID {part_id} не найден")
        
        return value
    
    def validate_customer_phone(self, value):
        """Валидация номера телефона"""
        # Убираем все пробелы и дефисы
        cleaned_phone = ''.join(filter(str.isdigit, value))
        if not cleaned_phone:
            raise serializers.ValidationError("Введите корректный номер телефона")
        return value
    
    def create(self, validated_data):
        """Создание заказа с позициями"""
        items_data = validated_data.pop('items')
        
        # Вычисляем общую сумму
        total_amount = 0
        for item_data in items_data:
            part_id = item_data['part_id']
            quantity = item_data['quantity']
            
            from catalog.models import Part
            part = Part.objects.get(id=part_id)
            unit_price = part.price_opt
            total_price = quantity * unit_price
            total_amount += total_price
            
            # Обновляем данные позиции
            item_data['unit_price'] = unit_price
            item_data['total_price'] = total_price
        
        # Создаем заказ
        order = Order.objects.create(
            total_amount=total_amount,
            **validated_data
        )
        
        # Создаем позиции заказа
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        # Создаем запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            comment='Заказ создан'
        )
        
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления заказа (только статус)"""
    
    class Meta:
        model = Order
        fields = ['status', 'notes']
    
    def update(self, instance, validated_data):
        """Обновление заказа с записью в историю"""
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # Обновляем заказ
        instance = super().update(instance, validated_data)
        
        # Если статус изменился, записываем в историю
        if old_status != new_status:
            OrderStatusHistory.objects.create(
                order=instance,
                status=new_status,
                comment=f"Статус изменен с '{instance.get_status_display()}' на '{instance.get_status_display()}'"
            )
        
        return instance


class OrderListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заказов (краткая информация)"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone',
            'total_amount', 'status', 'status_display', 'items_count',
            'created_at'
        ]
    
    def get_items_count(self, obj):
        """Количество позиций в заказе"""
        return obj.items.count()








