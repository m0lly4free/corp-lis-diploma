from django.db import models
from django.urls import reverse

class News(models.Model):
    """Модель для новостей компании"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    content = models.TextField(verbose_name='Основной текст')
    short_description = models.TextField(verbose_name='Краткий анонс')
    image = models.ImageField(upload_to='news/', verbose_name='Основное изображение', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})