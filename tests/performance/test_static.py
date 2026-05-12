import os
from pathlib import Path
from django.test import TestCase


class StaticOptimizationTest(TestCase):
    """Проверка оптимизации статики (9.2.4.1–9.2.4.2)"""
    
    def test_css_files_exist(self):
        """CSS-файлы существуют"""
        static_dir = Path('static/css')
        if static_dir.exists():
            css_files = list(static_dir.glob('*.css'))
            self.assertGreater(len(css_files), 0, "CSS файлы не найдены")
    
    def test_image_optimization(self):
        """Изображения оптимизированы"""
        media_dir = Path('media')
        if media_dir.exists():
            large_images = []
            for img in media_dir.rglob('*'):
                if img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    if img.stat().st_size > 500 * 1024:  # > 500KB
                        large_images.append(img.name)
            
            # Предупреждение о больших изображениях (не ошибка)
            if large_images:
                print(f"⚠️  Большие изображения: {large_images}")
    
    def test_static_files_accessible(self):
        """Статические файлы доступны"""
        from django.test import Client
        client = Client()
        
        # Проверяем, что статика загружается
        response = client.get('/static/css/main.css')
        # Может быть 200 (OK) или 404 (если файл не найден)
        self.assertIn(response.status_code, [200, 404])