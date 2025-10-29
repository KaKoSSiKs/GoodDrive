from rest_framework import serializers
from .models import SeoPage, SeoSettings


class SeoPageSerializer(serializers.ModelSerializer):
    """Сериализатор для SEO страниц"""
    og_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SeoPage
        fields = [
            'slug', 'title', 'description', 'keywords',
            'og_title', 'og_description', 'og_image_url',
            'canonical_url', 'robots', 'yandex_verification',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_og_image_url(self, obj):
        """Возвращает URL изображения для Open Graph"""
        return obj.get_og_image_url


class SeoSettingsSerializer(serializers.ModelSerializer):
    """Сериализатор для SEO настроек"""
    default_og_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SeoSettings
        fields = [
            'site_name', 'site_description', 'default_og_image_url',
            'yandex_verification', 'google_verification',
            'yandex_metrica', 'google_analytics',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_default_og_image_url(self, obj):
        """Возвращает URL изображения по умолчанию"""
        if obj.default_og_image:
            return obj.default_og_image.url
        return None








