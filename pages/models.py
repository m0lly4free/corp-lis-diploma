from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from core.fields import MediaImageField

class Page(models.Model):
    """Модель для управления основными страницами сайта"""
    
    # Основные поля страницы
    title = models.CharField(max_length=255, verbose_name='Название страницы')
    slug = models.SlugField(unique=True, verbose_name='Слаг', help_text='URL-часть страницы (автоматически генерируется из названия)')
    content = models.TextField(verbose_name='Текстовое содержимое')
    
    # SEO-мета-данные
    meta_title = models.CharField(max_length=255, verbose_name='SEO Заголовок (meta title)', blank=True)
    meta_description = models.TextField(verbose_name='SEO Описание (meta description)', blank=True)
    meta_keywords = models.CharField(max_length=255, verbose_name='SEO Ключевые слова (meta keywords)', blank=True)
    
    # Служебные поля
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['title']
        db_table = 'pages'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматическая генерация slug, если не указан
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)