from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["id", "title", "description", "image_url"]

    def get_image_url(self, obj):
        image_field = getattr(obj, 'image', None)
        if image_field:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(image_field.url)
            return image_field.url
        return None