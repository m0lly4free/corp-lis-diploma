from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from core.fields import MediaImageField
@classmethod
def get_active_pages(cls):
    return cls.objects.filter(is_active=True).select_related()
class Page(models.Model):
    """Модель для управления основными страницами сайта"""
    
    # Основные поля страницы
    title = models.CharField(max_length=255, verbose_name=_('Название страницы'))
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('Слаг'), 
        help_text=_('URL-часть страницы (автоматически генерируется из названия)')
    )
    content = models.TextField(verbose_name=_('Текстовое содержимое'))
    
    # SEO-мета-данные
    meta_title = models.CharField(
        max_length=255, 
        verbose_name=_('SEO Заголовок (meta title)'), 
        blank=True
    )
    meta_description = models.TextField(
        verbose_name=_('SEO Описание (meta description)'), 
        blank=True
    )
    meta_keywords = models.CharField(
        max_length=255, 
        verbose_name=_('SEO Ключевые слова (meta keywords)'), 
        blank=True
    )
    
    # Служебные поля
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата последнего изменения'))
    version = models.IntegerField(default=0, editable=False)
    
    class Meta:
        verbose_name = _('Страница')
        verbose_name_plural = _('Страницы')
        ordering = ['title']
        db_table = 'pages'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматическая генерация slug, если не указан
        if not self.slug:
            self.slug = slugify(self.title)
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)
        
        # Автоматическое обновление sitemap при сохранении
        from django.contrib.sitemaps import ping_google
        try:
            ping_google()
        except Exception:
            pass  # Игнорируем ошибки пинга Google
    
    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'slug': self.slug})