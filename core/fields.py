import os
from PIL import Image
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from .validators import validate_file_extension, validate_file_size
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class MediaFileField(models.FileField):
    """Кастомное поле для медиафайлов с валидацией"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [validate_file_extension, validate_file_size])
        kwargs.setdefault('storage', FileSystemStorage())
        super().__init__(*args, **kwargs)

class MediaImageField(models.ImageField):
    """Кастомное поле для изображений с валидацией и миниатюрами"""
    
    def __init__(self, *args, **kwargs):
        # Настройки по умолчанию
        self.max_size = kwargs.pop('max_size', (1920, 1080))
        self.quality = kwargs.pop('quality', 85)
        self.formats = kwargs.pop('formats', ['JPEG', 'PNG', 'WEBP'])
        
        # Ограничения на размер файла (10MB по умолчанию)
        self.max_upload_size = kwargs.pop('max_upload_size', 10 * 1024 * 1024)  # 10MB
        
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """
        Валидация и оптимизация изображения при загрузке
        """
        # Выполняем стандартную валидацию
        value = super().clean(value, model_instance)
        
        if value:
            # Проверка размера файла
            if value.size > self.max_upload_size:
                raise ValidationError(
                    _('Размер файла не должен превышать %(max_size)s MB.'),
                    params={'max_size': self.max_upload_size // (1024 * 1024)}
                )
            
            # Проверка формата файла
            try:
                image = Image.open(value)
                if image.format not in self.formats:
                    raise ValidationError(
                        _('Неподдерживаемый формат изображения. Допустимые форматы: %(formats)s.'),
                        params={'formats': ', '.join(self.formats)}
                    )
            except Exception as e:
                raise ValidationError(_('Некорректный файл изображения.'))
        
        return value
    
    def save_form_data(self, instance, data):
        """
        Сохранение и оптимизация изображения
        """
        if data and hasattr(data, 'file'):
            # Открываем изображение
            image = Image.open(data.file)
            
            # Конвертируем в RGB если необходимо (для JPEG/WebP)
            if image.mode in ('RGBA', 'LA', 'P') and 'JPEG' in self.formats:
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Изменяем размер, если необходимо
            if image.width > self.max_size[0] or image.height > self.max_size[1]:
                image.thumbnail(self.max_size, Image.Resampling.LANCZOS)
            
            # Сохраняем оптимизированное изображение
            from io import BytesIO
            from django.core.files.base import ContentFile
            
            buffer = BytesIO()
            
            # Определяем формат сохранения
            save_format = 'JPEG'
            if image.mode == 'RGBA':
                save_format = 'PNG'
            elif 'WEBP' in self.formats:
                save_format = 'WEBP'
            
            # Сохраняем в буфер
            if save_format == 'JPEG':
                image.save(buffer, format=save_format, quality=self.quality, optimize=True)
            elif save_format == 'WEBP':
                image.save(buffer, format=save_format, quality=self.quality, optimize=True)
            else:
                image.save(buffer, format=save_format, optimize=True)
            
            # Заменяем оригинальный файл оптимизированным
            data.file = ContentFile(buffer.getvalue())
            data.name = self._get_optimized_filename(data.name, save_format.lower())
        
        super().save_form_data(instance, data)
    
    def _get_optimized_filename(self, original_name, new_extension):
        """
        Генерация имени файла с новым расширением
        """
        name, ext = os.path.splitext(original_name)
        return f"{name}.{new_extension}"