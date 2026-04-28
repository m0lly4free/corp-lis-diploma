import os
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Оптимизирует изображения в MEDIA_ROOT для веба (JPEG quality=85, max 1920px)'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            self.stdout.write(self.style.WARNING('MEDIA_ROOT не найден.'))
            return

        optimized = 0
        for root, _, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    path = os.path.join(root, file)
                    try:
                        with Image.open(path) as img:
                            # Конвертация RGBA/P в RGB для JPEG
                            if img.mode in ('RGBA', 'LA', 'P'):
                                bg = Image.new('RGB', img.size, (255, 255, 255))
                                bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                                img = bg
                            
                            # Ограничение размера
                            if img.width > 1920 or img.height > 1080:
                                img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                            
                            # Сохранение с оптимизацией
                            img.save(path, 'JPEG', quality=85, optimize=True)
                            optimized += 1
                    except Exception as e:
                        logger.warning(f'Не удалось оптимизировать {path}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Оптимизировано изображений: {optimized}'))