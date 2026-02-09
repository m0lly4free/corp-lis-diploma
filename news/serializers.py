from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    preview_image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ["id", "title", "content", "preview_image_url", "created_at"]

    def get_preview_image_url(self, obj):
        if obj.preview_image:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.preview_image.url) if request else obj.preview_image.url
        return None