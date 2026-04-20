from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    """Модель для ролей пользователей"""
    ADMIN = 'admin'
    EDITOR = 'editor'
    
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (EDITOR, 'Редактор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EDITOR, verbose_name='Роль')
    
    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'