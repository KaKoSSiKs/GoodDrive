from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Notification, NotificationSettings
from .serializers import NotificationSerializer, NotificationSettingsSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet для уведомлений"""
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по прочитанности
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Фильтр по типу
        notification_type = self.request.query_params.get('type')
        if notification_type:
            queryset = queryset.filter(type=notification_type)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Количество непрочитанных уведомлений"""
        count = Notification.objects.filter(is_read=False).count()
        return Response({'count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Отметить уведомление как прочитанное"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked_read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Отметить все уведомления как прочитанные"""
        Notification.objects.filter(is_read=False).update(is_read=True)
        return Response({'status': 'all_marked_read'})
    
    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        """Очистить все уведомления"""
        Notification.objects.all().delete()
        return Response({'status': 'cleared'})


class NotificationSettingsViewSet(viewsets.ViewSet):
    """ViewSet для настроек уведомлений"""
    
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Получить настройки"""
        # Для простоты используем дефолтные настройки
        # В реальном приложении нужна привязка к пользователю
        settings, _ = NotificationSettings.objects.get_or_create(
            user_id=1,  # Временно хардкодим
            defaults={
                'notification_email': '89227081553@mail.ru'
            }
        )
        serializer = NotificationSettingsSerializer(settings)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Обновить настройки"""
        settings, _ = NotificationSettings.objects.get_or_create(user_id=1)
        serializer = NotificationSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

