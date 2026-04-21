from rest_framework import serializers
from services.models import Service
from news.models import News
from contacts.models import ContactMessage
from pages.models import Page

class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для услуг"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'description', 'short_description', 
            'category', 'category_display', 'image', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для новостей"""
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'short_description', 
            'image', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ContactMessageSerializer(serializers.ModelSerializer):
    """Сериализатор для формы обратной связи"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'message': {'required': True, 'allow_blank': False}
        }
    
    def validate_email(self, value):
        """Валидация email"""
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("Некорректный формат email адреса.")

class PageSerializer(serializers.ModelSerializer):
    """Сериализатор для статических страниц"""
    
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'content', 'meta_title', 
            'meta_description', 'meta_keywords', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']