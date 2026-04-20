import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from services.models import Service
from news.models import News
from core.utils import create_thumbnail

@receiver(post_save, sender=Service)
def create_service_thumbnail(sender, instance, **kwargs):
    """Создание миниатюры для изображения услуги"""
    if instance.image:
        create_thumbnail(instance.image.path)

@receiver(post_save, sender=News)
def create_news_thumbnail(sender, instance, **kwargs):
    """Создание миниатюры для изображения новости"""
    if instance.image:
        create_thumbnail(instance.image.path)

@receiver(post_delete, sender=Service)
def delete_service_files(sender, instance, **kwargs):
    """Удаление файлов при удалении услуги"""
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)
        # Удаляем миниатюру
        name, ext = os.path.splitext(instance.image.path)
        thumbnail_path = f"{name}_thumb{ext}"
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

@receiver(post_delete, sender=News)
def delete_news_files(sender, instance, **kwargs):
    """Удаление файлов при удалении новости"""
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)
        # Удаляем миниатюру
        name, ext = os.path.splitext(instance.image.path)
        thumbnail_path = f"{name}_thumb{ext}"
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)