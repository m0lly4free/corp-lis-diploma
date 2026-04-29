from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from core.fields import MediaImageField
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging
import bleach

logger = logging.getLogger('system_errors')


class Service(models.Model):
    """Модель для услуг компании с защитой от XSS"""
    
    PURCHASE = 'purchase'
    DISMANTLING = 'dismantling'
    SELF_TRANSPORT = 'self_transport'
    PRODUCTION = 'production'
    SALES = 'sales'
    CONSULTING = 'consulting'
    
    CATEGORY_CHOICES = [
        (PURCHASE, _('Покупка лома')),
        (DISMANTLING, _('Демонтаж')),
        (SELF_TRANSPORT, _('Самовывоз')),
        (PRODUCTION, _('Производство')),
        (SALES, _('Продажа')),
        (CONSULTING, _('Консультации')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Название услуги'))
    slug = models.SlugField(
        unique=True, 
        db_index=True,
        verbose_name=_('Слаг')
    )
    description = models.TextField(verbose_name=_('Подробное описание'))
    short_description = models.TextField(verbose_name=_('Краткое описание'))
    
    category = models.CharField(
        max_length=100, 
        choices=CATEGORY_CHOICES, 
        verbose_name=_('Категория'),
        db_index=True
    )
    
    image = MediaImageField(
        upload_to='services/',  
        verbose_name=_('Изображение'), 
        null=True, 
        blank=True,
        max_upload_size=5*1024*1024,  
        formats=['JPEG', 'JPG', 'PNG', 'SVG'], 
        quality=85
    )
    
    is_active = models.BooleanField(
        default=True, 
        db_index=True,
        verbose_name=_('Активна')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    version = models.IntegerField(default=0, editable=False)
    
    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active', 'name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})
    
    @classmethod
    def get_active_services(cls):
        return cls.objects.filter(is_active=True).order_by('name')
    
    def save(self, *args, **kwargs):
        # 🔒 ОЧИСТКА HTML ОТ ОПАСНЫХ ТЕГОВ (Защита от XSS - ТЗ 5.3)
        if self.description:
            # Разрешаем только безопасные HTML-теги
            allowed_tags = [
                'p', 'br', 'strong', 'em', 'u', 'b', 'i',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li',
                'a', 'img', 'blockquote', 'code', 'pre'
            ]
            
            # Разрешаем только безопасные атрибуты
            allowed_attributes = {
                'a': ['href', 'title', 'target'],
                'img': ['src', 'alt', 'title', 'width', 'height'],
            }
            
            # Разрешаем только безопасные протоколы
            allowed_protocols = ['http', 'https', 'mailto']
            
            # Очищаем HTML
            self.description = bleach.clean(
                self.description,
                tags=allowed_tags,
                attributes=allowed_attributes,
                protocols=allowed_protocols,
                strip=True,
                strip_comments=True
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
        
        # Генерация slug
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Обновление версии
        if self.pk:
            self.version += 1
        
        super().save(*args, **kwargs)
        
        # ping_google() вынесен в on_commit
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
@receiver([post_save, post_delete], sender='services.Service')
def invalidate_service_cache(sender, instance, **kwargs):
    """
    Автоматическая очистка кеша при изменении/удалении услуги.
    """
    try:
        cache.delete_pattern('*services*')
        cache.delete_pattern('*corp_lis*')
        logger.info(f"Cache invalidated for Service: {instance}")
    except (AttributeError, NotImplementedError):
        cache.clear()
        logger.warning(f"Pattern delete failed, full cache clear triggered")
    except Exception as e:
        logger.error(f"Cache invalidation error: {str(e)}")