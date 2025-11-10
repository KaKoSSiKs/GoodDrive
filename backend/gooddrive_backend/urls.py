from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_auth import admin_login, admin_verify, admin_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # Admin API endpoints
    path('api/admin/login/', admin_login, name='admin-login'),
    path('api/admin/verify/', admin_verify, name='admin-verify'),
    path('api/admin/logout/', admin_logout, name='admin-logout'),
    # Main API
    # path('api/', include('files.urls')),  # Временно отключено - модель не определена
    path('api/', include('catalog.urls')),
    path('api/', include('seo.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('finance.urls')),
    path('api/', include('crm.urls')),
    path('robots.txt', include('seo.urls')),
    path('sitemap.xml', include('seo.urls')),
    path('yandex-verification.html', include('seo.urls')),
]

# Обслуживание медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
