from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('files.urls')),  # Временно отключено - модель не определена
    path('api/', include('catalog.urls')),
    path('api/', include('seo.urls')),
    path('api/', include('orders.urls')),
    path('robots.txt', include('seo.urls')),
    path('sitemap.xml', include('seo.urls')),
    path('yandex-verification.html', include('seo.urls')),
]

# Обслуживание медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
