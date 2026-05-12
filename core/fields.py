import os
import unicodedata
from PIL import Image
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class MediaFileField(models.FileField):
    """Кастомное поле для медиафайлов с валидацией"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [])
        kwargs.setdefault('storage', FileSystemStorage())
        super().__init__(*args, **kwargs)

class MediaImageField(models.ImageField):
    """
    Кастомное поле для изображений с валидацией и миниатюрами.
    Соответствует ТЗ 5.6: ограничения на загрузку медиафайлов.
    """
    
    def __init__(self, *args, **kwargs):
        # Настройки по умолчанию
        self.max_size = kwargs.pop('max_size', (1920, 1080))
        self.quality = kwargs.pop('quality', 85)
        # 🔒 ТЗ 5.6.1: JPG, JPEG, PNG, SVG
        self.formats = kwargs.pop('formats', ['JPEG', 'JPG', 'PNG', 'SVG'])
        
        # 🔒 ТЗ 5.6.2: Макс. размер 5MB
        self.max_upload_size = kwargs.pop('max_upload_size', 5 * 1024 * 1024)
        
        super().__init__(*args, **kwargs)
    
    def deconstruct(self):
        """
        Обязательно для миграций!
        Сериализует кастомные параметры поля.
        """
        name, path, args, kwargs = super().deconstruct()
        kwargs['max_size'] = self.max_size
        kwargs['quality'] = self.quality
        kwargs['formats'] = self.formats
        kwargs['max_upload_size'] = self.max_upload_size
        return name, path, args, kwargs
    
    def clean(self, value, model_instance):
        """
        Валидация и оптимизация изображения при загрузке.
        ТЗ 5.6.1, 5.6.2, 5.6.3
        """
        value = super().clean(value, model_instance)
        
        if value:
            # 🔒 5.6.2: Проверка размера файла
            if value.size > self.max_upload_size:
                raise ValidationError(
                    _('Размер файла не должен превышать %(max_size)s МБ.'),
                    params={'max_size': self.max_upload_size // (1024 * 1024)}
                )
            
            # 🔒 5.6.1: Проверка формата файла
            try:
                image = Image.open(value)
                if image.format not in self.formats:
                    raise ValidationError(
                        _('Неподдерживаемый формат. Допустимые: %(formats)s.'),
                        params={'formats': ', '.join(self.formats)}
                    )
                image.verify()  # 🔒 5.6.3: Проверка целостности
                value.file.seek(0)  # Сброс указателя после verify()
            except Exception:
                raise ValidationError(_('Некорректный файл изображения.'))
        
        return value
    
    def generate_filename(self, instance, filename):
        """
        🔒 ТЗ 5.6.4.3: Нормализация имени файла
        - Кириллица → транслит
        - Спецсимволы → дефисы
        - Удаление опасных символов
        """
        name, ext = os.path.splitext(filename)
        name = os.path.basename(name)
        
        # Транслитерация + очистка
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        name = ''.join(c if c.isalnum() or c == '-' else '-' for c in name)
        name = '-'.join(filter(None, name.split('-')))
        
        # Ограничение длины
        if len(name) > 50:
            name = name[:50]
        
        safe_name = f"{name.lower()}{ext.lower()}" if name else f"img_{os.urandom(4).hex()}{ext.lower()}"
        
        return super().generate_filename(instance, safe_name)
    
    def save_form_data(self, instance, data):
        """
        Сохранение и оптимизация изображения.
        (Твой рабочий код)
        """
        if data and hasattr(data, 'file'):
            image = Image.open(data.file)
            
            # Конвертируем в RGB если необходимо
            if image.mode in ('RGBA', 'LA', 'P') and 'JPEG' in self.formats:
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Изменяем размер
            if image.width > self.max_size[0] or image.height > self.max_size[1]:
                image.thumbnail(self.max_size, Image.Resampling.LANCZOS)
            
            # Сохраняем оптимизированное
            from io import BytesIO
            from django.core.files.base import ContentFile
            
            buffer = BytesIO()
            
            save_format = 'JPEG'
            if image.mode == 'RGBA':
                save_format = 'PNG'
            elif 'WEBP' in self.formats:
                save_format = 'WEBP'
            
            if save_format == 'JPEG':
                image.save(buffer, format=save_format, quality=self.quality, optimize=True)
            elif save_format == 'WEBP':
                image.save(buffer, format=save_format, quality=self.quality, optimize=True)
            else:
                image.save(buffer, format=save_format, optimize=True)
            
            data.file = ContentFile(buffer.getvalue())
            data.name = self._get_optimized_filename(data.name, save_format.lower())
        
        super().save_form_data(instance, data)
    
    def _get_optimized_filename(self, original_name, new_extension):
        """Генерация имени файла с новым расширением"""
        name, ext = os.path.splitext(original_name)
        return f"{name}.{new_extension}"