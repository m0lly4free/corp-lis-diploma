from django.db import models
from django.urls import reverse
from core.fields import MediaImageField

class News(models.Model):
    """Модель для новостей компании"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    content = models.TextField(verbose_name='Основной текст')
    short_description = models.TextField(verbose_name='Краткий анонс', blank=True)
    image = MediaImageField(upload_to='news/', verbose_name='Изображение', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
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
        super().save(*args, **kwargs)