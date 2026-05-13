from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    # Используем безопасное получение поля (image или preview_image)
    preview_image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        # Добавляем slug, если он нужен в API, иначе оставляем как есть
        fields = ["id", "title", "slug", "content", "preview_image_url", "created_at"]

    def get_preview_image_url(self, obj):
        # Проверяем существование поля через getattr, чтобы избежать AttributeError
        image_field = getattr(obj, 'image', None) or getattr(obj, 'preview_image', None)
        if image_field:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(image_field.url)
            return image_field.url
        return None