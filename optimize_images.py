import os
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def optimize_image(image_path, quality=85, max_width=1920, max_height=1080):
    """Оптимизирует изображение для веба"""
    try:
        with Image.open(image_path) as img:
            # Конвертируем в RGB если необходимо
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Изменяем размер если необходимо
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Сохраняем с оптимизацией
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            logger.info(f"Optimized image: {image_path}")
            
    except Exception as e:
        logger.error(f"Error optimizing image {image_path}: {str(e)}")

def optimize_media_directory(media_root):
    """Оптимизирует все изображения в директории media"""
    supported_formats = ('.jpg', '.jpeg', '.png')
    
    for root, dirs, files in os.walk(media_root):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_path = os.path.join(root, file)
                optimize_image(image_path)

if __name__ == "__main__":
    # Запуск оптимизации
    from django.conf import settings
    optimize_media_directory(settings.MEDIA_ROOT)