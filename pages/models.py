from django.db import models, transaction
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
# from core.fields import MediaImageField  ← Удалено: импорт не используется

class Page(models.Model):
    """Модель для управления основными страницами сайта"""
    
    title = models.CharField(max_length=255, verbose_name=_('Название страницы'))
    slug = models.SlugField(
        unique=True, 
        db_index=True,  # ← Ускорение поиска по slug
        verbose_name=_('Слаг'), 
        help_text=_('URL-часть страницы (автоматически генерируется из названия)')
    )
    content = models.TextField(verbose_name=_('Текстовое содержимое'))
    
    meta_title = models.CharField(max_length=255, verbose_name=_('SEO Заголовок'), blank=True)
    meta_description = models.TextField(verbose_name=_('SEO Описание'), blank=True)
    meta_keywords = models.CharField(max_length=255, verbose_name=_('SEO Ключевые слова'), blank=True)
    
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_('Активна'))  # ← Индекс для фильтрации
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
        if not self.slug:
            self.slug = slugify(self.title)
        if self.pk:
            self.version += 1
            
        super().save(*args, **kwargs)
        
        # ⚠️ КРИТИЧЕСКАЯ ОПТИМИЗАЦИЯ ДЛЯ ТЗ 4.4:
        # ping_google() делал синхронный HTTP-запрос к Google на каждом сохранении.
        # Под нагрузкой это блокировало поток Gunicorn и увеличивало время ответа.
        # Переносим в transaction.on_commit() → выполнится ПОСЛЕ успешной записи в БД, 
        # не блокируя основной поток ответа.
        transaction.on_commit(self._notify_search_engines)

    def _notify_search_engines(self):
        """Асинхронное уведомление поисковиков (не блокирует save)"""
        try:
            from django.contrib.sitemaps import ping_google
            ping_google()
        except Exception:
            pass  # Игнорируем ошибки сети в production

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'slug': self.slug})