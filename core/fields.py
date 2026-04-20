from django.db import models
from django.core.files.storage import FileSystemStorage
from .validators import validate_file_extension, validate_file_size

class MediaFileField(models.FileField):
    """Кастомное поле для медиафайлов с валидацией"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [validate_file_extension, validate_file_size])
        kwargs.setdefault('storage', FileSystemStorage())
        super().__init__(*args, **kwargs)

class MediaImageField(models.ImageField):
    """Кастомное поле для изображений с валидацией и миниатюрами"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [validate_file_extension, validate_file_size])
        kwargs.setdefault('storage', FileSystemStorage())
        super().__init__(*args, **kwargs)