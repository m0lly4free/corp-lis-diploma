from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для статических страниц.
    Используется в API для получения контента страниц.
    """
    class Meta:
        model = Page
        # Добавьте все необходимые поля модели Page
        fields = ['id', 'slug', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']