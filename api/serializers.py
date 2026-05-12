from rest_framework import serializers
from services.models import Service
from news.models import News
from contacts.models import ContactMessage
from pages.models import Page
import re

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
    """Сериализатор для формы обратной связи с защитой от спама"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'message': {'required': True, 'allow_blank': False}
        }
    
    def validate_name(self, value):
        """Валидация имени - защита от спама"""
        if len(value) < 2:
            raise serializers.ValidationError("Имя должно содержать минимум 2 символа.")
        
        # Проверка на наличие только букв и пробелов
        if not re.match(r'^[а-яА-Яa-zA-Z\s]+$', value):
            raise serializers.ValidationError("Имя может содержать только буквы и пробелы.")
        
        return value
    
    def validate_message(self, value):
        """Валидация сообщения - защита от спама"""
        if len(value) < 10:
            raise serializers.ValidationError("Сообщение должно содержать минимум 10 символов.")
        
        # Проверка на количество ссылок (спам часто содержит много ссылок)
        url_count = len(re.findall(r'http[s]?://|www\.', value))
        if url_count > 2:
            raise serializers.ValidationError("Сообщение содержит слишком много ссылок.")
        
        return value
    
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