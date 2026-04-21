from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.fields import MediaImageField

class Service(models.Model):
    """Модель для услуг компании"""
    
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
    slug = models.SlugField(unique=True, verbose_name=_('Слаг'))
    description = models.TextField(verbose_name=_('Подробное описание'))
    short_description = models.TextField(verbose_name=_('Краткое описание'))
    category = models.CharField(
        max_length=100, 
        choices=CATEGORY_CHOICES, 
        verbose_name=_('Категория')
    )
    image = MediaImageField(
        upload_to='services/', 
        verbose_name=_('Основное изображение'), 
        null=True, 
        blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    version = models.IntegerField(default=0, editable=False)
    
    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)