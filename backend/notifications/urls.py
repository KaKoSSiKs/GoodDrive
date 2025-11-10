from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NotificationSettingsViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('notification-settings/', NotificationSettingsViewSet.as_view({'get': 'list', 'put': 'update'}), name='notification-settings'),
]

