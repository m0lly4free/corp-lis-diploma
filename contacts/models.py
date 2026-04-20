from django.db import models
from django.core.validators import EmailValidator

class ContactMessage(models.Model):
    """Модель для хранения обращений с формы контактов"""
    
    # Основные поля обращения
    name = models.CharField(max_length=255, verbose_name='Имя отправителя')
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True)
    email = models.EmailField(verbose_name='E-mail', validators=[EmailValidator()])
    message = models.TextField(verbose_name='Текст обращения')
    
    # Статус обработки
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')
    
    # Служебные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    
    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-created_at']
        db_table = 'contact_messages'

    def __str__(self):
        return f'Обращение от {self.name} ({self.email})'