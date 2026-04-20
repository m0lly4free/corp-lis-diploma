import os
from PIL import Image
from django.conf import settings

def create_thumbnail(image_path, thumbnail_size=(300, 300)):
    """
    Создает миниатюру для изображения
    """
    if not os.path.exists(image_path):
        return None
        
    # Получаем директорию и имя файла
    directory = os.path.dirname(image_path)
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    
    # Создаем имя для миниатюры
    thumbnail_name = f"{name}_thumb{ext}"
    thumbnail_path = os.path.join(directory, thumbnail_name)
    
    try:
        with Image.open(image_path) as img:
            # Конвертируем в RGB если необходимо (для JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Создаем миниатюру
            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, quality=85, optimize=True)
            
        return thumbnail_path
    except Exception as e:
        print(f"Ошибка при создании миниатюры: {e}")
        return None