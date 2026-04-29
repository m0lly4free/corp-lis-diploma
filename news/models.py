from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.fields import MediaImageField
import logging
import bleach

logger = logging.getLogger('system_errors')


class News(models.Model):
    """Модель для новостей компании с защитой от XSS"""
    
    title = models.CharField(max_length=255, verbose_name=_('Заголовок'), db_index=True)
    slug = models.SlugField(
        unique=True, 
        db_index=True,
        verbose_name=_('Слаг')
    )
    content = models.TextField(verbose_name=_('Основной текст'))
    short_description = models.TextField(verbose_name=_('Краткий анонс'), blank=True)
    
    image = MediaImageField(
        upload_to='news/',
        verbose_name=_('Изображение'), 
        null=True, 
        blank=True,
        max_upload_size=5*1024*1024,  # ← 5 МБ
        formats=['JPEG', 'JPG', 'PNG', 'SVG'], 
        quality=85
    )
    
    is_active = models.BooleanField(
        default=True, 
        db_index=True,
        verbose_name=_('Активна')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    version = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')
        ordering = ['-created_at']
        db_table = 'news'
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
            models.Index(fields=['slug', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    @classmethod
    def get_active_news(cls):
        return cls.objects.filter(is_active=True).order_by('-created_at')

    def save(self, *args, **kwargs):
        # 🔒 ОЧИСТКА HTML ОТ ОПАСНЫХ ТЕГОВ (Защита от XSS - ТЗ 5.3)
        if self.content:
            # Разрешаем только безопасные HTML-теги
            allowed_tags = [
                'p', 'br', 'strong', 'em', 'u', 'b', 'i',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li',
                'a', 'img', 'blockquote', 'code', 'pre'
            ]
            
            # Разрешаем только безопасные атрибуты для ссылок и изображений
            allowed_attributes = {
                'a': ['href', 'title', 'target'],
                'img': ['src', 'alt', 'title', 'width', 'height'],
            }
            
            # Разрешаем только безопасные протоколы для ссылок
            allowed_protocols = ['http', 'https', 'mailto']
            
            # Очищаем HTML
            self.content = bleach.clean(
                self.content,
                tags=allowed_tags,
                attributes=allowed_attributes,
                protocols=allowed_protocols,
                strip=True,  # Удаляем опасные теги (не экранируем)
                strip_comments=True  # Удаляем HTML-комментарии
            )
        
        # Очистка short_description
        if self.short_description:
            self.short_description = bleach.clean(
                self.short_description,
                tags=['p', 'br', 'strong', 'em', 'b', 'i'],
                attributes={},
                strip=True,
                strip_comments=True
            )
        
        # Автоматическое заполнение short_description, если не указано
        if not self.short_description and self.content:
            # Удаляем HTML-теги для краткого описания
            clean_text = bleach.clean(self.content, tags=[], strip=True)
            self.short_description = (
                clean_text[:200] + '...' if len(clean_text) > 200 else clean_text
            )
        
        # Обновление версии при редактировании
        if self.pk:
            self.version += 1
            
        super().save(*args, **kwargs)
        
        # ✅ ping_google() вынесен в on_commit
        transaction.on_commit(self._notify_search_engines)

    def _notify_search_engines(self):
        """Асинхронное уведомление поисковиков"""
        try:
            from django.contrib.sitemaps import ping_google
            ping_google()
        except Exception:
            pass


# ==========================================
# Сигналы для инвалидации кеша (ТЗ 4.4)
# ==========================================
@receiver([post_save, post_delete], sender='news.News')
def invalidate_news_cache(sender, instance, **kwargs):
    """
    Автоматическая очистка кеша при изменении/удалении новости.
    """
    try:
        cache.delete_pattern('*news*')
        cache.delete_pattern('*corp_lis*')
        logger.info(f"Cache invalidated for News: {instance}")
    except (AttributeError, NotImplementedError):
        cache.clear()
        logger.warning(f"Pattern delete failed, full cache clear triggered")
    except Exception as e:
        logger.error(f"Cache invalidation error: {str(e)}")