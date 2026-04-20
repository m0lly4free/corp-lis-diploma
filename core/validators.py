import os
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_file_extension(value):
    """Проверка расширения файла"""
    ext = os.path.splitext(value.name)[1].lower()
    
    allowed_extensions = []
    allowed_extensions.extend(['.' + ext for ext in getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', [])])
    allowed_extensions.extend(['.' + ext for ext in getattr(settings, 'ALLOWED_DOCUMENT_EXTENSIONS', [])])
    
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Недопустимый формат файла. Разрешены: {", ".join(allowed_extensions)}'
        )

def validate_file_size(value):
    """Проверка размера файла"""
    max_size = getattr(settings, 'MAX_FILE_SIZE', 5 * 1024 * 1024) 
    
    if value.size > max_size:
        raise ValidationError(
            f'Размер файла не должен превышать {max_size // (1024 * 1024)} МБ.'
        )