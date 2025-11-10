from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .import_views import upload_part_image, import_from_excel, download_excel_template

router = DefaultRouter()
router.register(r'brands', views.BrandViewSet)
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'parts', views.PartViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('parts/upload-image/', upload_part_image, name='upload-part-image'),
    path('parts/import-excel/', import_from_excel, name='import-excel'),
    path('parts/excel-template/', download_excel_template, name='excel-template'),
]








