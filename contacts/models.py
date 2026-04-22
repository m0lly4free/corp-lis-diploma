from django.db import models
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

class ContactMessage(models.Model):
    """Модель для хранения обращений с формы контактов"""
    
    # Основные поля обращения
    name = models.CharField(max_length=255, verbose_name=_('Имя отправителя'))
    phone = models.CharField(max_length=50, verbose_name=_('Телефон'), blank=True)
    email = models.EmailField(
        verbose_name=_('E-mail'), 
        validators=[EmailValidator()]
    )
    message = models.TextField(verbose_name=_('Текст обращения'))
    
    # Статус обработки
    is_processed = models.BooleanField(default=False, verbose_name=_('Обработано'))
    
    # IP-адрес отправителя для логирования и блокировок
    ip_address = models.GenericIPAddressField(verbose_name=_('IP адрес'), null=True, blank=True)
    
    # Служебные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата отправки'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата последнего обновления'))
    version = models.IntegerField(default=0, editable=False)
    
    class Meta:
        verbose_name = _('Обращение')
        verbose_name_plural = _('Обращения')
        ordering = ['-created_at']
        db_table = 'contact_messages'

    def __str__(self):
        return f'{_("Обращение от")} {self.name} ({self.email})'
    
    def save(self, *args, **kwargs):
        # Проверка на пустые поля перед сохранением
        if not self.name or not self.email or not self.message:
            raise ValidationError(_('Все обязательные поля должны быть заполнены'))
        
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)