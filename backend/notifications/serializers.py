from rest_framework import serializers
from .models import Notification, NotificationSettings


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомлений"""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'type_display',
            'priority',
            'priority_display',
            'title',
            'message',
            'link',
            'is_read',
            'related_order_id',
            'related_part_id',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NotificationSettingsSerializer(serializers.ModelSerializer):
    """Сериализатор настроек уведомлений"""
    
    class Meta:
        model = NotificationSettings
        fields = [
            'email_new_order',
            'email_low_stock',
            'push_new_order',
            'push_low_stock',
            'sound_enabled',
            'notification_email'
        ]

