from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.fields import MediaImageField
@classmethod
def get_active_news(cls):
    return cls.objects.filter(is_active=True).select_related()
class News(models.Model):
    """Модель для новостей компании"""
    title = models.CharField(max_length=255, verbose_name=_('Заголовок'))
    slug = models.SlugField(unique=True, verbose_name=_('Слаг'))
    content = models.TextField(verbose_name=_('Основной текст'))
    short_description = models.TextField(verbose_name=_('Краткий анонс'), blank=True)
    image = MediaImageField(
        upload_to='news/', 
        verbose_name=_('Изображение'), 
        null=True, 
        blank=True,
        max_size=(1920, 1080),
        quality=85,
        max_upload_size=10*1024*1024,  # 10MB
        formats=['JPEG', 'PNG', 'WEBP']
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    version = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')
        ordering = ['-created_at']
        db_table = 'news'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Автоматическое заполнение short_description, если не указано
        if not self.short_description and self.content:
            self.short_description = self.content[:200] + '...' if len(self.content) > 200 else self.content
        
        # Обновление версии при редактировании
        if self.pk:
            self.version += 1
            
        super().save(*args, **kwargs)
        
        # Автоматическое обновление sitemap при сохранении
        from django.contrib.sitemaps import ping_google
        try:
            ping_google()
        except Exception:
            pass  # Игнорируем ошибки пинга Google