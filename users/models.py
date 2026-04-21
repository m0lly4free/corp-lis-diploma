from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserRole(models.Model):
    """Модель для ролей пользователей"""
    ADMIN = 'admin'
    EDITOR = 'editor'
    
    ROLE_CHOICES = [
        (ADMIN, _('Администратор')),
        (EDITOR, _('Редактор')),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_role',
        verbose_name=_('Пользователь')
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default=EDITOR, 
        verbose_name=_('Роль')
    )
    version = models.IntegerField(default=0, editable=False)
    
    class Meta:
        verbose_name = _('Роль пользователя')
        verbose_name_plural = _('Роли пользователей')

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)