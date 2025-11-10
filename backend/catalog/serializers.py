from rest_framework import serializers
from .models import Brand, Warehouse, Part, PartImage


class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Brand"""
    parts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'site', 'parts_count']
        read_only_fields = ['id']
    
    def get_parts_count(self, obj):
        return obj.parts.filter(is_active=True).count()


class WarehouseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Warehouse"""
    parts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'parts_count']
        read_only_fields = ['id']
    
    def get_parts_count(self, obj):
        return obj.parts.filter(is_active=True).count()


class PartImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PartImage"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PartImage
        fields = ['id', 'image_url', 'alt_text', 'order_index']
        read_only_fields = ['id']
    
    def get_image_url(self, obj):
        """Возвращает URL изображения"""
        return obj.get_image_url


class PartListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка автозапчастей (краткая информация)"""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    main_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Part
        fields = [
            'id', 'is_active', 'title', 'label', 'original_number', 
            'manufacturer_number', 'brand_name', 'warehouse_name',
            'quantity', 'stock', 'reserve', 'available', 'price_opt',
            'main_image', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_main_image(self, obj):
        """Получаем первое изображение автозапчасти"""
        first_image = obj.images.first()
        if first_image:
            return {
                'url': first_image.image_url,
                'alt': first_image.alt_text
            }
        return None


class PartDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации об автозапчасти"""
    brand = BrandSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    images = PartImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Part
        fields = [
            'id', 'is_active', 'title', 'label', 'original_number',
            'manufacturer_number', 'brand', 'warehouse', 'quantity',
            'stock', 'reserve', 'available', 'price_opt', 'description',
            'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PartCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления автозапчастей"""
    images = PartImageSerializer(many=True, required=False, read_only=True)
    brand_name = serializers.CharField(write_only=True, required=False)
    warehouse_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Part
        fields = [
            'is_active', 'title', 'label', 'original_number',
            'manufacturer_number', 'brand', 'brand_name', 'warehouse', 
            'warehouse_name', 'quantity', 'stock', 'reserve', 'price_opt', 
            'cost_price', 'description', 'images'
        ]
    
    def create(self, validated_data):
        # Обработка brand_name - создаём бренд если указан
        brand_name = validated_data.pop('brand_name', None)
        if brand_name and not validated_data.get('brand'):
            brand, _ = Brand.objects.get_or_create(
                name=brand_name,
                defaults={'country': 'Не указана'}
            )
            validated_data['brand'] = brand
        
        # Обработка warehouse_name - создаём склад если указан
        warehouse_name = validated_data.pop('warehouse_name', None)
        if warehouse_name and not validated_data.get('warehouse'):
            warehouse, _ = Warehouse.objects.get_or_create(
                name=warehouse_name,
                defaults={'address': 'Не указан'}
            )
            validated_data['warehouse'] = warehouse
        
        images_data = validated_data.pop('images', [])
        part = Part.objects.create(**validated_data)
        
        for image_data in images_data:
            PartImage.objects.create(part=part, **image_data)
        
        return part
    
    def update(self, instance, validated_data):
        # Обработка brand_name
        brand_name = validated_data.pop('brand_name', None)
        if brand_name:
            brand, _ = Brand.objects.get_or_create(
                name=brand_name,
                defaults={'country': 'Не указана'}
            )
            validated_data['brand'] = brand
        
        # Обработка warehouse_name
        warehouse_name = validated_data.pop('warehouse_name', None)
        if warehouse_name:
            warehouse, _ = Warehouse.objects.get_or_create(
                name=warehouse_name,
                defaults={'address': 'Не указан'}
            )
            validated_data['warehouse'] = warehouse
        
        images_data = validated_data.pop('images', [])
        
        # Обновляем основную информацию
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Обновляем изображения
        if images_data:
            # Удаляем старые изображения
            instance.images.all().delete()
            # Создаем новые
            for image_data in images_data:
                PartImage.objects.create(part=instance, **image_data)
        
        return instance
