from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CustomerNoteViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'customer-notes', CustomerNoteViewSet, basename='customer-note')

urlpatterns = [
    path('', include(router.urls)),
]

