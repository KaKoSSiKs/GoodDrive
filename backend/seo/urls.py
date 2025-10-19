from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pages', views.SeoPageViewSet)
router.register(r'settings', views.SeoSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('meta/<slug:slug>/', views.SeoPageViewSet.as_view({'get': 'meta'}), name='seo-meta'),
    path('robots.txt', views.robots_txt, name='robots-txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap-xml'),
    path('yandex-verification.html', views.yandex_verification, name='yandex-verification'),
]

