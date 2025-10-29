from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'brands', views.BrandViewSet)
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'parts', views.PartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]








