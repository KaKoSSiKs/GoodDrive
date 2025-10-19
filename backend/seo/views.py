from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from .models import SeoPage, SeoSettings
from .serializers import SeoPageSerializer, SeoSettingsSerializer


class SeoPageViewSet(viewsets.ModelViewSet):
    """ViewSet для управления SEO страницами"""
    queryset = SeoPage.objects.filter(is_active=True)
    serializer_class = SeoPageSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        """Возвращаем только активные страницы"""
        return SeoPage.objects.filter(is_active=True)
    
    @action(detail=True, methods=['get'])
    def meta(self, request, slug=None):
        """Получить SEO метаданные для конкретной страницы"""
        try:
            page = self.get_object()
            serializer = self.get_serializer(page)
            return Response(serializer.data)
        except SeoPage.DoesNotExist:
            # Возвращаем дефолтные метаданные
            settings_obj = SeoSettings.get_settings()
            default_data = {
                'slug': slug,
                'title': f"{settings_obj.site_name} - {slug.title()}",
                'description': settings_obj.site_description,
                'keywords': '',
                'og_title': f"{settings_obj.site_name} - {slug.title()}",
                'og_description': settings_obj.site_description,
                'og_image_url': settings_obj.default_og_image.url if settings_obj.default_og_image else None,
                'canonical_url': None,
                'robots': 'index, follow',
                'yandex_verification': settings_obj.yandex_verification,
                'is_active': True
            }
            return Response(default_data)


class SeoSettingsViewSet(viewsets.ModelViewSet):
    """ViewSet для управления SEO настройками"""
    queryset = SeoSettings.objects.all()
    serializer_class = SeoSettingsSerializer
    
    def get_object(self):
        """Возвращаем единственную запись настроек"""
        return SeoSettings.get_settings()
    
    def list(self, request, *args, **kwargs):
        """Возвращаем единственную запись настроек"""
        settings_obj = self.get_object()
        serializer = self.get_serializer(settings_obj)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Возвращаем единственную запись настроек"""
        settings_obj = self.get_object()
        serializer = self.get_serializer(settings_obj)
        return Response(serializer.data)


def robots_txt(request):
    """Генерирует robots.txt"""
    settings_obj = SeoSettings.get_settings()
    
    robots_content = f"""User-agent: *
Allow: /

User-agent: Yandex
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: {request.build_absolute_uri('/sitemap.xml')}
"""
    
    return HttpResponse(robots_content, content_type='text/plain')


def sitemap_xml(request):
    """Генерирует sitemap.xml"""
    from django.contrib.sites.models import Site
    from django.urls import reverse
    from catalog.models import Part, Brand
    
    try:
        current_site = Site.objects.get_current()
        domain = current_site.domain
    except:
        domain = request.get_host()
    
    base_url = f"https://{domain}"
    
    # Статические страницы
    static_pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'url': '/catalog/', 'priority': '0.9', 'changefreq': 'daily'},
        {'url': '/about/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/contact/', 'priority': '0.7', 'changefreq': 'monthly'},
    ]
    
    # Динамические страницы автозапчастей
    parts = Part.objects.filter(is_active=True).select_related('brand')
    part_pages = []
    for part in parts:
        part_pages.append({
            'url': f'/catalog/part/{part.id}/',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': part.updated_at.strftime('%Y-%m-%d')
        })
    
    # Страницы брендов
    brands = Brand.objects.all()
    brand_pages = []
    for brand in brands:
        brand_pages.append({
            'url': f'/catalog/brand/{brand.id}/',
            'priority': '0.6',
            'changefreq': 'weekly'
        })
    
    context = {
        'base_url': base_url,
        'static_pages': static_pages,
        'part_pages': part_pages,
        'brand_pages': brand_pages,
    }
    
    sitemap_content = render_to_string('seo/sitemap.xml', context)
    return HttpResponse(sitemap_content, content_type='application/xml')


def yandex_verification(request):
    """Страница подтверждения Яндекс.Вебмастер"""
    settings_obj = SeoSettings.get_settings()
    verification_code = settings_obj.yandex_verification
    
    if verification_code:
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Подтверждение Яндекс.Вебмастер</title>
</head>
<body>
    <p>Код подтверждения: {verification_code}</p>
</body>
</html>
"""
        return HttpResponse(html_content, content_type='text/html')
    else:
        return HttpResponse("Код подтверждения не настроен", status=404)

