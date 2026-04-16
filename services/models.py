from django.db import models
from django.urls import reverse

class Service(models.Model):
    """Модель для услуг компании"""
    name = models.CharField(max_length=255, verbose_name='Название услуги')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Подробное описание')
    short_description = models.TextField(verbose_name='Краткое описание')
    category = models.CharField(max_length=100, verbose_name='Категория', choices=(
        ('purchase', 'Покупка лома'),
        ('dismantling', 'Демонтаж'),
        ('self_transport', 'Самовывоз'),
        ('production', 'Производство'),
        ('sales', 'Продажа'),
        ('consulting', 'Консультации'),
    ))
    image = models.ImageField(upload_to='services/', verbose_name='Основное изображение', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})