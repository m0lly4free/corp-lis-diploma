from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)

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
    
    def _sync_permissions(self):
        """Автоматически назначает системные права Django на основе выбранной роли"""
        # Гарантируем доступ в админку
        self.user.is_staff = True
        
        if self.role == self.ADMIN:
            # Админ = полный доступ
            self.user.is_superuser = True
            self.user.save(update_fields=['is_staff', 'is_superuser'])
            self.user.user_permissions.clear()
            logger.info(f"✅ Admin permissions applied to {self.user.username}")
            return

        # Редактор = ограниченный доступ
        self.user.is_superuser = False
        self.user.save(update_fields=['is_staff', 'is_superuser'])
        
        # Импорты внутри метода, чтобы избежать циклических зависимостей
        from news.models import News
        from services.models import Service
        from pages.models import Page
        from contacts.models import ContactMessage
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        allowed_models = [News, Service, Page, ContactMessage]
        perms_to_add = []

        for model in allowed_models:
            ct = ContentType.objects.get_for_model(model)
            # Права: добавление, изменение, просмотр (удаление НЕ даём)
            codenames = [
                f'add_{model._meta.model_name}',
                f'change_{model._meta.model_name}',
                f'view_{model._meta.model_name}'
            ]
            perms = Permission.objects.filter(content_type=ct, codename__in=codenames)
            perms_to_add.extend(perms)

        # Полностью заменяем старые права на новые
        self.user.user_permissions.set(perms_to_add)
        logger.info(f"✅ Editor permissions synced for {self.user.username} ({len(perms_to_add)} rights)")

    def save(self, *args, **kwargs):
        # Обновляем версию
        if self.pk:
            self.version += 1
            
        # Сначала сохраняем запись роли
        super().save(*args, **kwargs)
        
        # После сохранения применяем права к пользователю
        try:
            self._sync_permissions()
        except Exception as e:
            logger.error(f" Permission sync failed for {self.user.username}: {e}")