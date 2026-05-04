from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

# Валидаторы вынесены на уровень модуля для чистоты и переиспользования
PHONE_REGEX = RegexValidator(
    regex=r'^\+?[0-9\s\-\(\)]{7,15}$',
    message=_("Введите корректный номер телефона (от 7 до 15 цифр).")
)

class ContactMessage(models.Model):
    """
    Модель для хранения обращений с формы контактов.
    Соответствует ТЗ 5.5: серверная валидация типа, длины, формата и обязательности.
    """
    
    name = models.CharField(
        max_length=255,
        verbose_name=_('Имя отправителя'),
        validators=[MinLengthValidator(2)]
    )
    
    email = models.EmailField(
        max_length=255,
        db_index=True,
        verbose_name=_('E-mail')
        # EmailField автоматически проверяет корректность формата
    )
    
    phone = models.CharField(
        max_length=50, 
        validators=[PHONE_REGEX],
        blank=True,
        null=True,
        verbose_name=_('Телефон')
    )
    
    message = models.TextField(
        verbose_name=_('Текст обращения'),
        validators=[MinLengthValidator(10)]
    )
    
    # Статус обработки
    is_processed = models.BooleanField(
        default=False,
        verbose_name=_('Обработано')
    )
    
    # IP-адрес отправителя
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP адрес'),
        null=True,
        blank=True
    )
    
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
        # Обновление версии при редактировании
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)